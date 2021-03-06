## train with states
set -ex
python bin_packing_baselines.py \
    --alg ppo2 \
    --num_env 16 \
    --num_timesteps 1000000 \
    --nsteps 256 \
    --noptepochs 10 \
    --nminibatches 16 \
    --save_interval 50 \
    --lr_type 'linear' \
    --max 1e-5 \
    --min 1e-5 \
    --ent_coef 0.005 \
    --network 'cnn2x' \
    --keys 'image' \
    --use_camera_obs True \
    --has_offscreen_renderer True \
    --camera_height 64 \
    --camera_width 64 \
    --test True \
    --log True \
    --random_take True \
    --debug 'new_version'
