# 📁 Upload Your Pig Videos Here

## ⭐ This is where you upload your training videos!

### Folder Structure

```
pig_training/
├── train/          ← Upload 80% of your videos here
│   ├── tail_biting/    ← Pigs biting tails (distress)
│   ├── ear_biting/     ← Pigs biting ears (distress)
│   ├── aggression/     ← Aggressive behavior (distress)
│   ├── eating/         ← Pigs eating (normal)
│   ├── sleeping/       ← Pigs sleeping (normal)
│   └── rooting/        ← Pigs rooting (normal)
├── val/            ← Upload 10% of your videos here (same structure)
└── test/           ← Upload 10% of your videos here (same structure)
```

### Instructions

1. **Organize your videos:**
   - **Distressed behaviors** → `tail_biting/`, `ear_biting/`, or `aggression/`
   - **Normal behaviors** → `eating/`, `sleeping/`, or `rooting/`

2. **Split your videos:**
   - 80% → `train/` folders
   - 10% → `val/` folders
   - 10% → `test/` folders

3. **Video requirements:**
   - Formats: `.mp4`, `.avi`, `.mov`, `.mkv`
   - Length: 10-60 seconds
   - Minimum: 50-100 videos per behavior class (more is better!)

### Behavior Classes

**Distress Behaviors:**
- `tail_biting` - Pigs biting other pigs' tails
- `ear_biting` - Pigs biting other pigs' ears
- `aggression` - Aggressive interactions between pigs

**Normal Behaviors:**
- `eating` - Pigs eating food
- `sleeping` - Pigs sleeping/resting
- `rooting` - Pigs rooting in substrate

### Next Steps

After uploading videos:
1. Run: `./scripts/run_all_steps.sh`
2. Wait for training to complete
3. Use your trained model!

See `README.md` in the project root for detailed instructions.

