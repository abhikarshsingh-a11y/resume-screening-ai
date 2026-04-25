def get_job_description():
    print("Paste the job description below.")
    print("When you are done, press Enter twice to finish.\n")

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)

    job_text = "\n".join(lines)
    return job_text


if __name__ == "__main__":
    text = get_job_description()
    print("\n--- Job Description Received ---")
    print(text)
    