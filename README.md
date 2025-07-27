## Author

This repository provides a QUBO-based framework for generating ligand binding poses within protein pockets to support structure-based virtual screening.

> **Reference:**  
> Pei-Kun Yang  
> Ligand Pose Generation via QUBO-Based Hotspot Sampling and Geometric Triplet Matching  
> E-mail: peikun@isu.edu.tw
> ORCID: https://orcid.org/0000-0003-1840-6204

## Repository Structure

- **1_CASF_2016/**  
  Prepares the dataset.  
  *Note: Due to storage constraints, only a sample (PDB ID: 1A30) is included in this repository.*

- **2_JH_Matrix/**  
  Computes the J and H matrices used in the QUBO formulation.

- **3_Dock/Dis_0.7_1.3/**  
  Demonstrates ligand docking using triplet-based geometric alignment, with `d̅ ± δ = 1.0 ± 0.3 Å` as an example.

## Dependencies

Make sure the following packages are installed before running the scripts:

```bash
pip install torch numpy autogrid4 autodock4
```
## Summary

The pipeline first selects energetically favorable grid points using a QUBO solver, then performs rigid-body alignment based on a three-atom geometric contour of the ligand. This modular setup allows easy tuning of matching thresholds and grid parameters, enabling control over the trade-off between accuracy and computational cost.

## License

This project is licensed under the [MIT License](LICENSE).
