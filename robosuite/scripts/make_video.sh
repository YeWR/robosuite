set -ex
python bin_packing_baselines2.py \
    --alg ppo2 \
    --num_env 16 \
    --num_timesteps 0 \
    --nsteps 256 \
    --noptepochs 10 \
    --nminibatches 32 \
    --lr_type 'linear' \
    --max 1e-4 \
    --min 1e-4 \
    --camera_height 64 \
    --camera_width 64 \
    --log True \
    --render_drop_freq 20 \
    --take_nums 8 \
    --use_typeVector True \
    --load_path 'results/BinPack-v0/version-1.2.0/image+depth/ppo2_cnn_type_linear_0.0001_0.0001_2000000total_256nsteps_10noptepochs_32batch_8take_Truetype_0.005ent_Falsedataset_64x64/checkpoints/00380' \
    --make_video True \
    --video_name 'demo.mp4' \
    --debug 'temp_video'