"""
Render Figure 1 (CCI + DAU overlay) and Figure 2 (activation funnel by channel)
for the Single-Creator Trap preliminary findings report.

Usage:
    cd Papers/CC6_20260410
    python figures/render.py

Outputs:
    figures/fig1_cci_dau.png  (+ .pdf)
    figures/fig2_activation_funnel.png  (+ .pdf)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def fig1_cci_dau():
    """Figure 1 — Creator Concentration Index over time, with DAU overlay (Phase 1)."""
    df = pd.read_csv(DATA_DIR / "baseline_phase1.csv", parse_dates=["date"])

    fig, ax_cci = plt.subplots(figsize=(11, 5))

    color_cci = "#d62728"
    color_dau = "#1f77b4"

    # CCI line on left axis
    ax_cci.set_xlabel("Date")
    ax_cci.set_ylabel("Creator Concentration Index (CCI)", color=color_cci)
    ax_cci.plot(
        df["date"], df["cci"],
        color=color_cci, marker="o", linewidth=2, zorder=3, label="CCI",
    )
    ax_cci.tick_params(axis="y", labelcolor=color_cci)
    ax_cci.set_ylim(0, 1.08)
    ax_cci.axhline(
        y=0.5, color="gray", linestyle="--", linewidth=1, alpha=0.6,
        label="CCI = 0.5 concentration threshold",
    )

    # Annotate CCI = 1.0 days (single-creator monopoly)
    for d, cci in zip(df["date"], df["cci"]):
        if cci >= 0.999:
            ax_cci.annotate(
                "CCI = 1.0",
                xy=(d, cci),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center",
                fontsize=9,
                color=color_cci,
                fontweight="bold",
            )

    # DAU bars on right axis
    ax_dau = ax_cci.twinx()
    ax_dau.set_ylabel("Daily Active Users (DAU)", color=color_dau)
    ax_dau.bar(
        df["date"], df["dau"],
        alpha=0.30, color=color_dau, width=0.75, zorder=1, label="DAU",
    )
    ax_dau.tick_params(axis="y", labelcolor=color_dau)

    # Annotate launch peak and collapse
    peak_idx = df["dau"].idxmax()
    ax_dau.annotate(
        f"Launch peak\nDAU = {int(df.loc[peak_idx, 'dau'])}",
        xy=(df.loc[peak_idx, "date"], df.loc[peak_idx, "dau"]),
        xytext=(15, -25),
        textcoords="offset points",
        ha="left",
        fontsize=9,
        color=color_dau,
        arrowprops=dict(arrowstyle="->", color=color_dau, alpha=0.6),
    )

    plt.title(
        "Figure 1 — Creator Concentration Index and Daily Active Users\n"
        "Phase 1 baseline: April 1–April 16, 2026 (N = 291 signups)",
        pad=12,
    )
    fig.autofmt_xdate(rotation=30)
    fig.tight_layout()

    out_png = OUT_DIR / "fig1_cci_dau.png"
    out_pdf = OUT_DIR / "fig1_cci_dau.pdf"
    fig.savefig(out_png, dpi=200, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out_png.name}")
    print(f"  ✓ {out_pdf.name}")


def fig2_activation_funnel():
    """Figure 2 — Activation funnel by signup channel (Phase 1).

    Highlights: first_friend = 0 for BOTH channels across all 291 signups.
    """
    df = pd.read_csv(DATA_DIR / "activation_phase1.csv")

    funnel_cols = [
        "signups", "first_ask", "first_post", "first_follow",
        "first_friend", "first_chat", "activated",
    ]
    funnel_labels = [
        "Signup", "First ask", "First post", "First follow",
        "First friend\n(mutual)", "First chat", "Activated",
    ]

    fig, ax = plt.subplots(figsize=(11, 5.5))

    x = list(range(len(funnel_cols)))
    width = 0.36

    invite = df[df["channel"] == "invite"][funnel_cols].values[0]
    firebase = df[df["channel"] == "firebase"][funnel_cols].values[0]

    bars_inv = ax.bar(
        [i - width / 2 for i in x], invite, width,
        label=f"Invite channel (N = {int(invite[0])})", color="#1f77b4",
    )
    bars_fb = ax.bar(
        [i + width / 2 for i in x], firebase, width,
        label=f"Firebase channel (N = {int(firebase[0])})", color="#ff7f0e",
    )

    # Annotate counts on each bar
    for bars in (bars_inv, bars_fb):
        for bar in bars:
            h = bar.get_height()
            ax.annotate(
                f"{int(h)}",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    # Highlight first_friend = 0 finding
    friend_idx = funnel_cols.index("first_friend")
    ax.annotate(
        "first_friend = 0\nfor both channels\n(zero mutual follows\nin 21 days, N = 291)",
        xy=(friend_idx, 0),
        xytext=(friend_idx, max(invite) * 0.4),
        ha="center",
        fontsize=10,
        color="#d62728",
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.5),
    )

    ax.set_xticks(x)
    ax.set_xticklabels(funnel_labels, rotation=20, ha="right")
    ax.set_ylabel("User count")
    ax.set_title(
        "Figure 2 — Activation funnel by signup channel\n"
        "Phase 1: 291 signups across 21 days (March 29 – April 15, 2026)",
        pad=12,
    )
    ax.legend(loc="upper right")
    ax.set_ylim(0, max(invite) * 1.18)

    fig.tight_layout()

    out_png = OUT_DIR / "fig2_activation_funnel.png"
    out_pdf = OUT_DIR / "fig2_activation_funnel.pdf"
    fig.savefig(out_png, dpi=200, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out_png.name}")
    print(f"  ✓ {out_pdf.name}")


if __name__ == "__main__":
    print(f"Rendering figures into {OUT_DIR}")
    fig1_cci_dau()
    fig2_activation_funnel()
    print("Done.")
