# GaFaR

GaFaR reconstructs faces from face-recognition templates using an EG3D generator and a learned mapping network. The official `idiap/gafar` repository is BSD-3-Clause and documents EG3D, `ffhqrebalanced512-128.pkl`, pretrained mapping networks, and ICCV 2023 / TPAMI citations.

Its reconstruction attack is not a key-agnostic protected-template set attack. A bounded future reproduction should use an official checkpoint and documented evaluation, not train EG3D from scratch. It needs a compatible GPU, lawful model assets, and the project evaluation data.
