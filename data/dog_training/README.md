# 📁 Upload Your Dog Videos Here

## ⭐ This is where you upload your training videos!

### Folder Structure

```
dog_training/
├── train/          ← Upload 80% of your videos here
│   ├── pacing/     ← Dogs pacing (distress behavior)
│   ├── scratching/← Dogs scratching (distress behavior)
│   ├── sleeping/  ← Dogs sleeping (normal behavior)
│   ├── walking/    ← Dogs walking (normal behavior)
│   └── resting/    ← Dogs resting (normal behavior)
├── val/            ← Upload 10% of your videos here (same structure)
└── test/           ← Upload 10% of your videos here (same structure)
```

### Instructions

1. **Organize your videos:**
   - **Distressed behaviors** → `pacing/` or `scratching/`
   - **Normal behaviors** → `sleeping/`, `walking/`, or `resting/`

2. **Split your videos:**
   - 80% → `train/` folders
   - 10% → `val/` folders
   - 10% → `test/` folders

3. **Video requirements:**
   - Formats: `.mp4`, `.avi`, `.mov`, `.mkv`
   - Length: 10-60 seconds
   - Minimum: 50-100 videos per behavior class (more is better!)

### Next Steps

After uploading videos:
1. Run: `./scripts/run_all_steps.sh`
2. Wait for training to complete
3. Use your trained model!

See `docs/EXACT_STEPS.md` for detailed instructions.
