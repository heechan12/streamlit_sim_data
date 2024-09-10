"""
예지 코드
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd

# pSIM APDU Commands
pSIM_FIRST_APDU_COMMAND = 'AA82022CA20900A4080C047FFF6F61A281FF00D60000FA'
pSIM_SECOND_APDU_COMMAND = 'A20900A4080C047FFF6F61A281FF00D600FAFA'
pSIM_THIRD_APDU_COMMAND = 'A20700A4080C022F30A20700D6000502'

# eSIM APDU Commands
eSIM_FIRST_APDU_COMMAND = 'AA82022C220900A4080C047FFF6F612281FF00D60000FA'
eSIM_SECOND_APDU_COMMAND = '220900A4080C047FFF6F612281FF00D600FAFA'
eSIM_THIRD_APDU_COMMAND = '220700A4080C022F30220700D6000502'


def decimal_to_hex(decimal_number):
    return hex(decimal_number)[2:].zfill(4)


def read_excel_as_pandas(file) -> pd.DataFrame:
    try:
        print("try")
        excel_file = pd.read_excel(file, sheet_name=1)
        return excel_file
    except Exception as e:
        messagebox.showerror("Error", f"Excel file Format Error")
        return None


def is_valid_sheet(excel_file: pd.DataFrame) -> bool:
    if excel_file is not None:
        d4_value = excel_file.iloc[2, 3]
        d103_value = excel_file.iloc[101, 3]
        h3_value = excel_file.iloc[1, 7]
        i3_value = excel_file.iloc[1, 8]
        j3_value = excel_file.iloc[1, 9]
    else:
        return False

    if d4_value == 1 and d103_value == 100 and h3_value == "MCC" and i3_value == "MNC" and j3_value == "AcT":
        return True
    else:
        return False


def edit_excel_data(excel_file: pd.DataFrame, first_command, second_command, third_command) -> str:
    if is_valid_sheet(excel_file):
        df = excel_file.copy()  # 원본 데이터를 변경하지 않기 위해 복사본 생성
        for col in df.columns:
            df[col] = df[col].map(lambda x: str(x).replace(' ', '') if pd.notnull(x) else x)

        data = df.iloc[2:102, 7:10].astype(str).values

        formatted_data = [[cell.ljust(3, 'F') if cell != 'nan' else 'nan' for cell in row] for row in data]
        for row in formatted_data:
            for idx, cell in enumerate(row):
                if cell == 'nan':
                    if idx == 2:
                        row[idx] = 'AAAA'
                    else:
                        row[idx] = 'AAA'

        expanded_data = [list(''.join(row)) for row in formatted_data]
        eSIM_column_order = [1, 0, 5, 2, 4, 3]
        reordered_data = [
            [row[i] for i in eSIM_column_order] + row[6:] for row in expanded_data
        ]

        combined_data = [''.join(row) for row in reordered_data]
        first_combined = ''.join(combined_data[:50])
        second_combined = ''.join(combined_data[50:])
        oplmn_list = first_combined + second_combined

        edited_code = first_command + first_combined + second_command + second_combined + third_command
        return edited_code, oplmn_list
    else:
        return 'invalid'



def get_result_code(code: str, version) -> str:
    version_hex = decimal_to_hex(version)
    if code is not None:
        return code + version_hex
    return '오류'


def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if filename:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filename)


def generate_code():
    file = entry_file.get()
    version = entry_version.get()

    if not file:
        messagebox.showwarning("Warning", "Please select an Excel file.")
        return

    try:
        version = int(version)
        if version <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid version number.")
        return

    excel_pd_file = read_excel_as_pandas(file)
    if excel_pd_file is not None:
        pSIM_code, pSIM_oplmn_list = edit_excel_data(excel_pd_file, pSIM_FIRST_APDU_COMMAND, pSIM_SECOND_APDU_COMMAND,
                                        pSIM_THIRD_APDU_COMMAND)
        eSIM_code, eSIM_oplmn_list = edit_excel_data(excel_pd_file, eSIM_FIRST_APDU_COMMAND, eSIM_SECOND_APDU_COMMAND,
                                   eSIM_THIRD_APDU_COMMAND)

        if pSIM_code != 'invalid' and eSIM_code != 'invalid':
            pSIM_result_code = get_result_code(pSIM_code, version)
            eSIM_result_code = get_result_code(eSIM_code, version)

            length_pSIM = len(pSIM_result_code) // 2  # pSIM code byte length
            length_eSIM = len(eSIM_result_code) // 2  # eSIM code byte length

            header_message_pSIM = f"{version}버전\n\n[USIM BIP msg.] 전체 Length : {length_pSIM}(짝수바이트), EF_OPLMN(5+95), EF_VER\n\n"
            header_message_eSIM = f"\n\n[eSIM BIP msg.] 전체 Length : {length_eSIM}(짝수바이트), EF_OPLMN(5+95), EF_VER\n\n"
            oplmn_list_str = f"{pSIM_oplmn_list}"

            final_output = header_message_pSIM + pSIM_result_code + header_message_eSIM + eSIM_result_code + "\n\n[EF_OPLMN 100/100]\n\n" + oplmn_list_str

            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, final_output)
        else:
            messagebox.showerror("Error", "Invalid Excel sheet format.")
    else:
        messagebox.showerror("Error", "Failed to read Excel file.")


def save_to_file():
    final_output = text_output.get(1.0, tk.END)
    if not final_output.strip():
        messagebox.showwarning("Warning", "No text to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(final_output)
        messagebox.showinfo("Info", "File saved successfully.")


# GUI Setup
root = tk.Tk()
root.title("국가 정보 업데이트_v0.6")
root.geometry("800x600")

label_file = tk.Label(root, text="엑셀 파일 Upload :")
label_file.grid(row=0, column=0, padx=10, pady=10, sticky='e')

entry_file = tk.Entry(root, width=50)
entry_file.grid(row=0, column=1, padx=10, pady=10, sticky='w')

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2, padx=10, pady=10, sticky='w')

label_version = tk.Label(root, text="버전 정보 입력 (ex. 10088) :")
label_version.grid(row=1, column=0, padx=10, pady=10, sticky='e')

entry_version = tk.Entry(root, width=10)
entry_version.grid(row=1, column=1, padx=10, pady=10, sticky='w')
entry_version.insert(0, "1")

button_generate = tk.Button(root, text="코드 생성", command=generate_code)
button_generate.grid(row=1, column=2, padx=10, pady=10, sticky='w')

text_output = scrolledtext.ScrolledText(root, width=95, height=30)
text_output.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

button_save = tk.Button(root, text="Save to File", command=save_to_file)
button_save.grid(row=3, column=2, padx=10, pady=10, sticky="e")

# Run the application
root.mainloop()