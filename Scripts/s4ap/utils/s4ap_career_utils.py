from careers.career_tuning import Career, CareerLevel, TunableCareerTrack
from random import random
from typing import Callable, Iterator, Tuple, Union, List
from services import get_instance_manager
from sims.sim_info import SimInfo
from sims4.resources import Types

class S4APCareerUtils:

    @classmethod
    def get_career_guid(cls, career: Career) -> Union[int, None]:
        if career is None:
            return None
        return getattr(career, 'guid64', None)

    @staticmethod
    def load_career_by_guid(career: Union[int, Career]) -> Union[Career, None]:
        if career is None:
            return None
        if isinstance(career, Career):
            return career
        try:
            career_guid = int(career)
        except Exception:
            return None  # invalid ID

        # Use the game's instance manager for careers
        career_manager = get_instance_manager(Types.CAREER)
        if career_manager is None:
            return None
        return career_manager.get(career_guid)

    @classmethod
    def get_all_careers_for_sim_gen(cls, sim_info: SimInfo, include_career_callback: Callable[[Career], bool]=None) -> Iterator[Career]:
        if sim_info is None:
            return tuple()
        career_tracker = sim_info.career_tracker
        if career_tracker is None:
            return tuple()

        for career in career_tracker.careers.values():
            if include_career_callback is not None and not include_career_callback(career):
                continue
            yield career

    @staticmethod
    def determine_entry_level_into_career_from_user_level(career: Career, desired_user_level: int) -> Tuple[
        Union[int, None], Union[int, None], Union[TunableCareerTrack, None]]:
        if career is None:
            return None, None, None
        track = S4APCareerUtils.get_starting_career_track(career)

    @classmethod
    def get_starting_career_track(cls, career: Career) -> Union[TunableCareerTrack, None]:
        """get_starting_career_track(career)

        Retrieve the starting Career Track of a Career.

        :param career: A career.
        :type career: Career
        :return: The starting Career Track of the Career or None if not found.
        :rtype: Union[TunableCareerTrack, None]
        """
        if career is None:
            return None
        return career.start_track

    @classmethod
    def determine_entry_level_into_career_track_by_user_level(cls, career_track: TunableCareerTrack,
                                                              desired_user_level: int) -> Tuple[
        Union[int, None], Union[int, None], Union[TunableCareerTrack, None]]:
        if career_track is None:
            return None, None, None
        track = career_track
        track_start_level = 1

        while True:
            track_length = len(cls.get_career_levels(track))
            level = desired_user_level - track_start_level
            if level < track_length:
                user_level = track_start_level + level
                return level, user_level, track

            branches = cls.get_branches(track)
            if not branches:
                # The exit path. When we run out of branches to check we'll just return the last info found.
                level = track_length - 1
                user_level = track_start_level + level
                return level, user_level, track

            track_start_level += track_length
            track = random.choice(branches)

    @classmethod
    def get_career_levels(cls, career_track: TunableCareerTrack, include_branches: bool = False) -> Tuple[CareerLevel]:
        if career_track is None:
            return tuple()
        if include_branches:
            if career_track is None:
                return tuple()
            if include_branches:
                # noinspection PyUnresolvedReferences
                if hasattr(career_track, 'career_levels') and career_track.career_levels is not None:
                    career_levels: List[CareerLevel] = list(career_track.career_levels)
                    branches = cls.get_branches(career_track)
                    for branch_career_track in branches:
                        sub_career_levels = cls.get_career_levels(branch_career_track,
                                                                  include_branches=include_branches)
                        if not sub_career_levels:
                            continue
                        career_levels.extend(sub_career_levels)
                    return tuple(career_levels)
            else:
                # noinspection PyUnresolvedReferences
                if hasattr(career_track, 'career_levels') and career_track.career_levels is not None:
                    return tuple(career_track.career_levels)
            return tuple()

    @classmethod
    def get_branches(cls, career_track: TunableCareerTrack, include_sub_branches: bool = False) -> Tuple[
        TunableCareerTrack]:
        """get_branches(career_track, include_sub_branches=True)

        Retrieve a collection of all Career Tracks that branch off of a Career Track and if specified, the branches those branches branch off to.

        :param career_track: A Career Track.
        :type career_track: TunableCareerTrack
        :param include_sub_branches: If True, all branches will be checked for their own branches and those branches will be included recursively. If False, only the top level branches will be included. Default is False.
        :type include_sub_branches: bool, optional
        :return: A collection of all Career Tracks that branch off from the specified Career Track.
        :rtype: Tuple[TunableCareerTrack]
        """
        if career_track is None:
            return tuple()
        if include_sub_branches:
            # noinspection PyUnresolvedReferences
            if hasattr(career_track, 'branches') and career_track.branches is not None:
                career_track_branches: List[TunableCareerTrack] = list(career_track.branches)
                for sub_career_track in career_track_branches:
                    sub_branches = cls.get_branches(sub_career_track, include_sub_branches=include_sub_branches)
                    if not sub_branches:
                        continue
                    career_track_branches.extend(sub_branches)
                return tuple(career_track_branches)
        else:
            # noinspection PyUnresolvedReferences
            if hasattr(career_track, 'branches') and career_track.branches is not None:
                return tuple(career_track.branches)
        return tuple()

    @staticmethod
    def get_work_performance(career: Career) -> float:
        """get_work_performance(career)

        Add an amount to the work performance of a career.

        :param career: The career to modify.
        :type career: Career
        :return: The amount of work performance acquired in the specified Career.
        :rtype: float
        """
        if career is None:
            return 0.0
        return career.work_performance