# -*- coding: utf-8 -*-
__author__ = 'whale'


class Parson:
    ID = None

    every_meet_flag = False
    meeting_paper = None
    mat_paper = None

    def __init__(self, id, num_of_people):
        self.ID = id
        self.init_paper(num_of_people)

    def init_paper(self, num_of_people):
        self.mat_paper = [0] * num_of_people
        self.meeting_paper = range(1, num_of_people + 1)
        self.meeting_paper.remove(self.ID)

    def meet(self, your_id):
        try:
            self.meeting_paper.remove(your_id)
        except:
            pass
        self.mat_paper[your_id - 1] += 1

    def get_meeting_count(self, your_id):
        return self.mat_paper[your_id]

    def get_meeting_paper(self):
        return self.meeting_paper


class Operator:
    NUM_OF_PEOPLE = None
    MAX_GROUP_PEOPLE = None

    parsons = None

    def __init__(self, num_of_people, max_group_people):
        self.NUM_OF_PEOPLE = num_of_people
        self.MAX_GROUP_PEOPLE = max_group_people
        self.parsons = self.generate_persons(num_of_people)

    def generate_persons(self, n):
        parson_list = []
        for i in range(1, n + 1):
            parson_list.append(Parson(i, n))
        return parson_list

    # 우리 그룹에서 가장 만나지 못한 사람.
    def all_unseen_people(self, current_group_list, mat_list):

        # 그룹을 모두 합치고
        temp_list = []
        for person in current_group_list:
            copy_meeting_paper = person.meeting_paper[:]
            for p in mat_list:
                try:
                    copy_meeting_paper.remove(p)
                except:
                    pass
            temp_list += copy_meeting_paper

        # 순회하면서 오브젝트에 각 이름별로 카운트
        temp_bucket = {}
        for e in temp_list:
            try:
                temp_bucket[e] += 1
            except:
                temp_bucket[e] = 0

        max_count = -1
        target = None
        # 카운트 된 것들 중에서 맥스인 친구를 반환.
        for e in temp_bucket:
            if temp_bucket[e] > max_count:
                target = e
                max_count = temp_bucket[e]

        return self.parsons[target - 1]

    def get_poor(self, parsons):
        poor = None
        max_count = -1
        for parson in parsons:
            if len(parson.meeting_paper) > max_count:
                max_count = len(parson.meeting_paper)
                poor = parson
        return poor

    def call_parsons(self, paper_list):
        parsons = []
        for id in paper_list:
            parsons.append(self.parsons[id - 1])
        return parsons

    def get_group(self):

        # 전체 그룹.
        group = []

        # 전체 사람 리스트를 만든다.
        all_list = range(1, self.NUM_OF_PEOPLE + 1)
        mat_list = []

        while not len(all_list) == 0:

            # 임시 그룹을 만든다.
            temp_group = []

            # 가장 많이 못 만난 사람을 찾는다.
            poor = self.get_poor(self.call_parsons(all_list))

            # 임시 그룹에 들어간다.
            temp_group.append(poor)

            while len(temp_group) < self.MAX_GROUP_PEOPLE:
                # 그룹에서 가장 많이 못 만난 사람을 찾아 그룹에 넣는다.
                new_partner = self.all_unseen_people(temp_group, mat_list)
                temp_group.append(new_partner)

                # 만났음을 상호 체크
                new_partner.meet(poor.ID)
                poor.meet(new_partner.ID)

            for parson in temp_group:
                all_list.remove(parson.ID)
                mat_list.append(parson.ID)

            # 하드코딩
            temp_group[1].meet(temp_group[2].ID)
            temp_group[2].meet(temp_group[1].ID)

            group.append(temp_group)

        # 프린팅
        for g in group:
            l = []
            for p in g:
                l.append(p.ID)
            print l

        return group

operator = Operator(9, 3)
operator.get_group()
print "===================="
operator.get_group()
print "===================="
operator.get_group()
print "===================="
operator.get_group()