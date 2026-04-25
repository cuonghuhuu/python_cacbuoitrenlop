from __future__ import annotations

import argparse
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import pandas as pd
    from matplotlib.ticker import FuncFormatter
except ImportError as exc:
    missing_package = exc.name or "required package"
    raise SystemExit(
        f"Missing dependency: {missing_package}. "
        "Install dependencies with: .\\.venv\\Scripts\\pip.exe install -r requirements.txt"
    ) from exc


DATE_COLUMN = "OrderDate"
REVENUE_COLUMN = "Sales"
CATEGORY_COLUMN = "Category"
CITY_COLUMN = "City"
STATE_COLUMN = "State"
COUNTRY_COLUMN = "Country"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ve cac bieu do thong ke doanh thu tu file CSV ban hang."
    )
    parser.add_argument(
        "--file",
        help="Duong dan toi file CSV. Neu bo trong, chuong trinh tu tim file CSV trong thu muc hien tai.",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Chi luu anh vao thu muc charts, khong mo cua so bieu do.",
    )
    return parser.parse_args()


def tim_file_csv(file_argument: str | None) -> Path:
    if file_argument:
        return Path(file_argument)

    csv_files = sorted(Path(".").glob("*.csv"))
    if len(csv_files) == 1:
        return csv_files[0]
    if not csv_files:
        raise SystemExit("Khong tim thay file CSV. Hay dung tham so --file de chi dinh file.")

    file_names = ", ".join(file.name for file in csv_files)
    raise SystemExit(f"Co nhieu file CSV: {file_names}. Hay dung --file de chon file can dung.")


def dinh_dang_tien_te(value: float, _position: float) -> str:
    return f"{value:,.0f}"


def doc_du_lieu(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path, encoding="utf-8-sig")

    required_columns = [
        DATE_COLUMN,
        REVENUE_COLUMN,
        CATEGORY_COLUMN,
        CITY_COLUMN,
        STATE_COLUMN,
        COUNTRY_COLUMN,
    ]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise SystemExit(f"File CSV thieu cac cot bat buoc: {missing_text}")

    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")
    if getattr(df[DATE_COLUMN].dt, "tz", None) is not None:
        df[DATE_COLUMN] = df[DATE_COLUMN].dt.tz_localize(None)

    df[REVENUE_COLUMN] = pd.to_numeric(df[REVENUE_COLUMN], errors="coerce")

    df["DiaChiBanHang"] = (
        df[CITY_COLUMN].fillna("").astype(str).str.strip()
        + ", "
        + df[STATE_COLUMN].fillna("").astype(str).str.strip()
        + ", "
        + df[COUNTRY_COLUMN].fillna("").astype(str).str.strip()
    )
    df["DiaChiBanHang"] = df["DiaChiBanHang"].str.strip(", ").str.replace(", ,", ",", regex=False)

    df = df.dropna(subset=[DATE_COLUMN, REVENUE_COLUMN]).copy()
    df["Thang"] = df[DATE_COLUMN].dt.to_period("M").astype(str)
    df["Nam"] = df[DATE_COLUMN].dt.year
    df["Quy"] = df[DATE_COLUMN].dt.to_period("Q").astype(str)
    return df.sort_values(DATE_COLUMN)


def tao_thu_muc_ket_qua() -> Path:
    output_dir = Path("charts")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def dinh_dang_bieu_do(ax, title: str, xlabel: str, ylabel: str = "Doanh thu") -> None:
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    ax.yaxis.set_major_formatter(FuncFormatter(dinh_dang_tien_te))


# Bai 1: Ve bieu do doanh thu theo thang
def ve_doanh_thu_theo_thang(df: pd.DataFrame, output_dir: Path) -> None:
    doanh_thu_thang = df.groupby("Thang")[REVENUE_COLUMN].sum()

    plt.figure(figsize=(14, 6))
    plt.plot(doanh_thu_thang.index, doanh_thu_thang.values, marker="o", linewidth=2.5, color="#1f77b4")
    dinh_dang_bieu_do(plt.gca(), "Doanh thu theo thang", "Thang")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "doanh_thu_theo_thang.png", dpi=300)


# Bai 2: Ve bieu do doanh thu theo nam
def ve_doanh_thu_theo_nam(df: pd.DataFrame, output_dir: Path) -> None:
    doanh_thu_nam = df.groupby("Nam")[REVENUE_COLUMN].sum()

    plt.figure(figsize=(10, 6))
    plt.bar(doanh_thu_nam.index.astype(str), doanh_thu_nam.values, color="#2ca02c")
    dinh_dang_bieu_do(plt.gca(), "Doanh thu theo nam", "Nam")
    plt.tight_layout()
    plt.savefig(output_dir / "doanh_thu_theo_nam.png", dpi=300)


# Bai 3: Ve bieu do doanh thu theo quy
def ve_doanh_thu_theo_quy(df: pd.DataFrame, output_dir: Path) -> None:
    doanh_thu_quy = df.groupby("Quy")[REVENUE_COLUMN].sum()

    plt.figure(figsize=(12, 6))
    plt.bar(doanh_thu_quy.index, doanh_thu_quy.values, color="#ff7f0e")
    dinh_dang_bieu_do(plt.gca(), "Doanh thu theo quy", "Quy")
    plt.xticks(rotation=35)
    plt.tight_layout()
    plt.savefig(output_dir / "doanh_thu_theo_quy.png", dpi=300)


# Bai 4: Ve bieu do doanh thu theo loai mat hang
def ve_doanh_thu_theo_loai_mat_hang(df: pd.DataFrame, output_dir: Path) -> None:
    doanh_thu_loai_hang = (
        df.groupby(CATEGORY_COLUMN)[REVENUE_COLUMN].sum().sort_values(ascending=True)
    )

    plt.figure(figsize=(10, 6))
    plt.barh(doanh_thu_loai_hang.index, doanh_thu_loai_hang.values, color="#9467bd")
    ax = plt.gca()
    ax.set_title("Doanh thu cac loai mat hang", fontsize=14, fontweight="bold")
    ax.set_xlabel("Doanh thu")
    ax.set_ylabel("Loai mat hang")
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_formatter(FuncFormatter(dinh_dang_tien_te))
    plt.tight_layout()
    plt.savefig(output_dir / "doanh_thu_theo_loai_mat_hang.png", dpi=300)


# Bai 5: Ve bieu do doanh thu theo dia chi ban hang
def ve_doanh_thu_theo_dia_chi(df: pd.DataFrame, output_dir: Path) -> None:
    doanh_thu_dia_chi = (
        df.groupby("DiaChiBanHang")[REVENUE_COLUMN].sum().sort_values(ascending=False).head(10)
    )
    doanh_thu_dia_chi = doanh_thu_dia_chi.sort_values(ascending=True)

    plt.figure(figsize=(12, 7))
    plt.barh(doanh_thu_dia_chi.index, doanh_thu_dia_chi.values, color="#8c564b")
    ax = plt.gca()
    ax.set_title("Top 10 dia chi ban hang co doanh thu cao nhat", fontsize=14, fontweight="bold")
    ax.set_xlabel("Doanh thu")
    ax.set_ylabel("Dia chi ban hang")
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_formatter(FuncFormatter(dinh_dang_tien_te))
    plt.tight_layout()
    plt.savefig(output_dir / "doanh_thu_theo_dia_chi.png", dpi=300)


def in_tom_tat(df: pd.DataFrame, file_path: Path, output_dir: Path) -> None:
    print(f"File CSV: {file_path.resolve()}")
    print(f"So dong hop le: {len(df):,}")
    print(f"Tong doanh thu: {df[REVENUE_COLUMN].sum():,.0f}")
    print(f"Tu ngay: {df[DATE_COLUMN].min().strftime('%d/%m/%Y')}")
    print(f"Den ngay: {df[DATE_COLUMN].max().strftime('%d/%m/%Y')}")
    print(f"Da luu cac bieu do trong thu muc: {output_dir.resolve()}")


def main() -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

    args = parse_args()
    file_path = tim_file_csv(args.file)
    output_dir = tao_thu_muc_ket_qua()
    df = doc_du_lieu(file_path)

    ve_doanh_thu_theo_thang(df, output_dir)
    ve_doanh_thu_theo_nam(df, output_dir)
    ve_doanh_thu_theo_quy(df, output_dir)
    ve_doanh_thu_theo_loai_mat_hang(df, output_dir)
    ve_doanh_thu_theo_dia_chi(df, output_dir)

    in_tom_tat(df, file_path, output_dir)

    if args.no_show:
        plt.close("all")
    else:
        plt.show()
        plt.close("all")


if __name__ == "__main__":
    main()
