text = input("入力してください: ")
def main():
    try:
        with open("output.txt", "w", encoding="utf-8") as f:
          f.write(text)
    except Exception as e:
        print(f"An error occurred: {e} ")
    return "Data written to output.txt"

if __name__ == "__main__":
    main()