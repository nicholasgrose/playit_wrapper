import subprocess
import sys


def main() -> None:
    process = start_playit()

    log("starting wrapper")

    while process.poll() is None:
        nextLine: str = process.stdout.readline().decode("utf-8")

        print(nextLine, end="")

        if playit_encountered_error(nextLine):
            log("restarting playit")
            process = restart_playit(process)


def log(message: str) -> None:
    print(f"WRAPPER: {message}")


def start_playit() -> subprocess.Popen:
    process = subprocess.Popen(
        ["playit", "-s"] + sys.argv[2:], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    log("started playit")

    return process


def playit_encountered_error(line: str) -> bool:
    return "SignatureError" in line


def restart_playit(playit_process: subprocess.Popen) -> subprocess.Popen:
    playit_process.kill()

    return start_playit()


if __name__ == "__main__":
    main()
