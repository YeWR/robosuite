set -ex
python bin_squeeze_baselines.py \
    --alg ppo2 \
    --num_env 1 \
    --num_timesteps 1200000 \
    --nsteps 1024 \
    --noptepochs 10 \
    --nminibatches 32 \
    --lr_type 'linear' \
    --max 1e-5 \
    --min 1e-5 \
    --network 'cnn' \
    --energy_tradeoff 0.8 \
    --ent_coef 0.2 \
    --place_num 3 \
    --log True \
    --debug 'debug'
