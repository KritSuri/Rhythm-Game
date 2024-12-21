import librosa
import numpy as np
import random
import csv

song_name = "Red"

def intersect_with_diff(base_list, comparing_list, threshold):
    '''intersect of 2 list that can tolerate slightly different value (the difference is equal or less than the threshold)'''
    output_list = []
    x = 0
    y = 0
    while (x < len(base_list)) and (y < len(comparing_list)):
        if abs(base_list[x] - comparing_list[y]) <= threshold:
            output_list.append(base_list[x])
            x += 1
            y += 1
        elif base_list[x] > comparing_list[y]:
            y += 1
        elif base_list[x] < comparing_list[y]:
            x += 1
    return output_list


class Beatmap_generator:
    def __init__(self, audio_path, meter=4, difficulty=5, t_prep=5, t_fade=5):
        self.audio_path = audio_path
        self.y, self.sr = librosa.load(self.audio_path)
        self.meter = meter
        self.level = difficulty
        self.t_prep = t_prep
        duration = librosa.get_duration(y=self.y)
        self.t_fade = duration - t_fade

        self.beat_times = self.find_beat_time()
        self.onset_times = self.find_onset_time()

        self.primary_beat_times1 = self.find_primary_beat1()
        self.primary_beat_times2 = self.find_primary_beat2()
        self.primary_beat_times = list(set(self.primary_beat_times1+self.primary_beat_times2))
        self.primary_beat_times.sort()

        self.secondary_beat_times = self.find_secondary_beat()

        self.beatmap = self.generate_beatmap()


    def find_beat_time(self):
        
        # get onset envelope
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr, aggregate=np.median)
        # get tempo and beats
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=self.sr)
        # we assume 4/4 time
        # meter = 4
        # calculate number of full measures 
        measures = (len(beats) // self.meter)
        # get onset strengths for the known beat positions
        # Note: this is somewhat naive, as the main strength may be *around*
        #       rather than *on* the detected beat position. 
        beat_strengths = onset_env[beats]
        # make sure we only consider full measures
        # and convert to 2d array with indices for measure and beatpos
        measure_beat_strengths = beat_strengths[:measures * self.meter].reshape(-1, self.meter)
        # add up strengths per beat position
        beat_pos_strength = np.sum(measure_beat_strengths, axis=0)
        # find the beat position with max strength
        downbeat_pos = np.argmax(beat_pos_strength)
        # convert the beat positions to the same 2d measure format
        full_measure_beats = beats[:measures * self.meter].reshape(-1, self.meter)
        # and select the beat position we want: downbeat_pos
        downbeat_frames = full_measure_beats[:, downbeat_pos]
        # print('Downbeat frames: {}'.format(downbeat_frames))
        # print times
        downbeat_times = librosa.frames_to_time(downbeat_frames, sr=self.sr)
        # print('Downbeat times in s: {}'.format(downbeat_times))
        return list(downbeat_times)

    def find_onset_time(self):
        y, sr = librosa.load(self.audio_path)
        onset_times = librosa.onset.onset_detect(y=y, sr=sr, units='time')
        return list(onset_times)

    def find_primary_beat1(self):
        primary_beat_times = intersect_with_diff(self.beat_times, self.onset_times, 0.35)
        primary_beat_times.sort()
        primary_beat_times = [i for i in primary_beat_times if (i>self.t_prep) and (i<self.t_fade)]
        return primary_beat_times

    def find_primary_beat2(self):
        half_beat_times = []
        for i in range(len(self.beat_times)-1):
            half = (self.beat_times[i+1] - self.beat_times[i])/2
            half_beat_times.append(self.beat_times[i]+half)
            primary_beat_times = intersect_with_diff(half_beat_times, self.onset_times, 0.35)
            primary_beat_times = [i for i in primary_beat_times if (i>self.t_prep) and (i<self.t_fade)]
        return primary_beat_times
    
    def find_secondary_beat(self):
        quater_beat_times = []
        for i in range(len(self.beat_times)-1):
            quater = (self.beat_times[i+1] - self.beat_times[i])/4
            quater_beat_times.append(self.beat_times[i] + quater)
            quater_beat_times.append(self.beat_times[i] + 3*quater)
            secondary_beat_times = intersect_with_diff(quater_beat_times, self.onset_times, 0.35)
            secondary_beat_times = [i for i in secondary_beat_times if (i>self.t_prep) and (i<self.t_fade)]
        return secondary_beat_times
    
    def action_weight(self, previous_action):
        '''only used to compute action weight when the game is fast'''
        if previous_action == [0, 0, 0, 0]:
            weight = (0, 10, 10, 10, 10, 10, 10)
        elif previous_action == [0, 1, 0, 0] or previous_action == [0, 0, 1, 0] or previous_action == [0, 1, 1, 0]: 
            weight = ((500-self.level*2), (10-self.level)+10, (10-self.level)+10, self.level, self.level, (10-self.level)+10, self.level)
        elif previous_action == [1, 0, 0, 0] or previous_action == [0, 0, 0, 1] or previous_action == [1, 0, 0, 1]:
            weight = ((500-self.level*2), self.level, self.level, (10-self.level)+10, (10-self.level)+10, self.level, (10-self.level)+10)
        return weight

    def generate_beatmap(self):

        beatmap = []
        # ['time', 'LEFT', 'DOWN', 'UP', 'LEFT'] 
        action_list = [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1]]
        
        # index 1 -> up
        # index 2 -> down
        # index 3 -> left
        # index 4 -> right
        # index 5 -> vertical
        # index 6 -> horizontal
        previous_beat = 0               # 0 = primary, 1 = secondary
        action_weight = (0, 20, 20, 20, 20, 20, 20)
        x = 0
        y = 0
        while (x < len(self.primary_beat_times)) and (y < len(self.secondary_beat_times)):
            if self.primary_beat_times[x] < self.secondary_beat_times[y]:
                if previous_beat == 0:
                    action = random.choices(action_list, weights=(400, 20, 20, 20, 20, 20, 20))
                    action_weight = self.action_weight(action[0])
                else:
                    action = random.choices(action_list, weights=action_weight)
                    action_weight = self.action_weight(action[0])
                previous_beat = 0
                beatmap.append([self.primary_beat_times[x]]+action[0])
                x += 1
            else:
                if previous_beat == 1:
                    action = random.choices(action_list, weights=(400, 20, 20, 20, 20, 20, 20))
                    action_weight = self.action_weight(action[0])
                else:
                    action = random.choices(action_list, weights=action_weight)
                    action_weight = self.action_weight(action[0])
                previous_beat = 1
                beatmap.append([self.secondary_beat_times[y]]+action[0])
                y += 1
            
        return beatmap

    def write_csv(self):
        fields = ['time', 'LEFT', 'DOWN', 'UP', 'LEFT'] 
        rows = self.beatmap
        with open("song\\"+song_name+"\\"+song_name+".csv", 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(rows)


class Beatmap_reader:
    def __init__(self):
        pass

song_path = "song\\"+song_name+"\\"+song_name+".mp3"
song = Beatmap_generator(song_path, 4)
song.write_csv()




