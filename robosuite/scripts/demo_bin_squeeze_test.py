import random
import time

import numpy as np
import robosuite as suite

from robosuite.wrappers import MyGymWrapper
from PIL import Image

def test_render_time(env):
    env.reset()

    ts = []
    ts_step = []
    for _ in range(30):

        action = env.action_space.sample()

        beg_tiem = time.time()
        env.step(action)
        end_time = time.time()

        ts_step.append(end_time - beg_tiem)

        beg_tiem = time.time()
        env.sim.render(width=256, height=256, camera_name='birdview')
        # env.sim.render(width=256, height=256, camera_name='agentview')
        end_time = time.time()

        ts.append(end_time - beg_tiem)

    ts = np.array(ts)
    ts_step = np.array(ts_step)

    print('Time: ', ts.mean())
    print('Time step: ', ts_step.mean())


def test_env_init(env):
    obs = env.reset()

    imgs = Image.fromarray(obs)
    imgs.show()


def test_step(env):
    obs = env.reset()

    action = env.action_space.sample()
    env.step(action)


def test_qpos_meaning(env):
    # create a video writer with imageio
    # writer = imageio.get_writer(video_path, fps=20)

    obs = env.reset()
    imgs = Image.fromarray(obs)
    imgs.show()

    action = np.array([0.2, 0.3])
    obs, rew, done, info = env.step(action)
    imgs = Image.fromarray(obs)
    imgs.show()


def test_video(env, video_path='demo/test/test.mp4'):

    import imageio
    writer = imageio.get_writer(video_path, fps=20)

    episodes = 4
    # action = env.action_space.sample()
    # action[0:3] = np.array([1., 0., 0.])
    action = np.array([0.4, 0.4, -1., 0., 0., 0., 0.])
    down = np.array([0.1, 0., -1.])
    for _ in range(episodes):
        env.reset()
        for i in range(50):
            # run a uniformly random agent
            # action = env.action_space.sample()

            # human policy
            # if i < 50:
            #     action[0:3] = down.copy()
            # elif i == 50:
            #     action = np.array([1., 0., 0., 0., 0., 0., 0.])
            # else:
            #     if i % 40 == 0:
            #         action[0:2] = -action[0:2]
            #     if i % 50 == 0:
            #         action[3:7] = -action[3:7]

            obs, reward, done, info = env.step(action)

            # contains depth
            if obs.shape[-1] == 4:
                image = obs[:, :, :-1]
                depth = obs[:, :, -1]

                import cv2
                depth_shape = depth.shape
                depth = depth.reshape(depth_shape[0], depth_shape[1], 1)
                depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR)

                obs = np.concatenate((image, depth), 0)

            writer.append_data(obs)
            print("Saving frame #{}".format(i))

            if done:
                break

    writer.close()


def adjust_camera_pos(env):
    env.reset()

    pos = np.array([1, 1, 1])
    for _ in range(1):
        action = env.action_space.sample()

        obs, rew, done, info = env.step(action)

        imgs = Image.fromarray(obs)
        imgs.show()

        # import ipdb
        # ipdb.set_trace()


def run(env):

    for _ in range(30):
        action = env.action_space.sample()
        obs, rew, done, info = env.step(action)

        import ipdb
        ipdb.set_trace()


def test_random_take(env):
    for _ in range(10):
        env.reset()

        for __ in range(100):
            action = env.action_space.sample()
            obs, rew, done, info = env.step(action)

            for i in range(200):
                env.render()

            if done:
                break


if __name__ == "__main__":

    from robosuite.scripts.hard_case import get_hard_cases

    case_train, case_test = get_hard_cases()

    env = suite.make(
        'BinSqueeze',
        has_renderer=False,
        has_offscreen_renderer=True,
        ignore_done=True,
        use_camera_obs=True,
        control_freq=20,
        camera_height=128,
        camera_width=128,
        camera_depth=True,
        test_cases=[],
    )


    # run(env)
    test_video(env)
    # adjust_camera_pos(env)