
# Bank Spiders Project

---

## How to use

1. Clone repo
2. Within cloned repo dir, use `python global_init.py` to make `init_all.bat`
3. Run `init_all.bat`
4. Grab a snack and wait
5. Project files are ready for use

---

## Starting spiders

- Use `extract_bats.bat` to copy each spider's `exec.bat` file into a folder called `bat_files`

- Select all files within `bat_files` dir and run them to launch the spiders.

---

## Getting results

- Use `extract_results.bat` to copy each spider's collected results into `results` dir

_**NOTE**_: this will delete anything in the `results` folder before copying the new results

---

## Sending collected results to S3 bucket

Make sure you have a `rootkey.csv` file in your local directory so that you have access to your AWS account

- Run `send_to_s3.bat`

---

Note: The spiders are meant to be used while their data is constantly being sent to S3.
This means that you can launch both the spiders and the S3 scripts at the same time.

---
