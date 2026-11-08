"""Display an existing UTF-8 execution log in a read-only window."""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="실행 로그 텍스트를 읽기 전용 창으로 엽니다.")
    parser.add_argument("log_file", type=Path, help="열 로그 파일의 경로")
    args = parser.parse_args()

    try:
        content = args.log_file.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        parser.error(f"로그 파일을 읽을 수 없습니다: {error}")

    import tkinter as tk

    root = tk.Tk()
    root.title("Python 기초 퀴즈 게임 — 실행 로그 / " + args.log_file.stem)
    height = min(780, max(430, len(content.splitlines()) * 24 + 70))
    root.geometry(f"1040x{height}+100+80")

    frame = tk.Frame(root, bg="#1e1e1e")
    frame.pack(fill="both", expand=True)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    text = tk.Text(
        frame, bg="#1e1e1e", fg="#eeeeee", font=("맑은 고딕", 13),
        padx=20, pady=16, borderwidth=0, highlightthickness=0,
        wrap="none", cursor="arrow", takefocus=False,
    )
    vertical = tk.Scrollbar(frame, orient="vertical", command=text.yview)
    horizontal = tk.Scrollbar(frame, orient="horizontal", command=text.xview)
    text.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
    text.grid(row=0, column=0, sticky="nsew")
    vertical.grid(row=0, column=1, sticky="ns")
    horizontal.grid(row=1, column=0, sticky="ew")
    text.insert("1.0", content)
    text.configure(state="disabled")
    root.mainloop()


if __name__ == "__main__":
    main()
