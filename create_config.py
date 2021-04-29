import argparse
import os
import random
import string
import uuid

from jinja2 import Environment, FileSystemLoader


def random_password(size):
    """Generate a random password"""
    random_source = string.ascii_letters + string.digits
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    for i in range(size):
        password += random.choice(random_source)
    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = "".join(password_list)
    return password


def main():

    """Example of a call: python create_config.py --mysql_host localhost --forwarded_allow_ip 192.168.0.101
    --pid_file /home/cquiros/ushauri.pid --error_log_file /home/cquiros/ushauri.log -d -c
    --repository_path /home/cquiros/tmp/ --odktools_path /home/cquiros/odktools --mysql_schema ushauri
    --mysql_user_name root --mysql_user_password 72EkBqCs! --ushauri_host localhost
    --ushauri_port 5900 /home/cquiros/test.ini"""

    parser = argparse.ArgumentParser()
    parser.add_argument("ini_path", help="Path to ini file to create")
    parser.add_argument("--mysql_host", required=True, help="MySQL host server to use")
    parser.add_argument(
        "--forwarded_allow_ip",
        required=True,
        help="IP of the proxy server calling Ushauri",
    )
    parser.add_argument(
        "--pid_file",
        required=True,
        help="File that will store the Ushauri process ID",
    )
    parser.add_argument(
        "--error_log_file",
        required=True,
        help="File that will store the Ushauri logs",
    )
    parser.add_argument(
        "-d",
        "--daemon",
        action="store_true",
        help="Start as Ushauri in detached mode",
    )
    parser.add_argument(
        "-c",
        "--capture_output",
        action="store_true",
        help="Start as Ushauri in detached mode",
    )
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="Overwrite if exists"
    )

    parser.add_argument(
        "--repository_path", required=True, help="Path to the Ushauri repository"
    )
    parser.add_argument("--odktools_path", required=True, help="Path to ODK Tools")
    parser.add_argument(
        "--mysql_port", default=3306, help="MySQL port to use. Default to 3306"
    )
    parser.add_argument(
        "--mysql_schema",
        default="ushauri",
        help="MySQL schema to use. Default to 'ushauri'",
    )
    parser.add_argument(
        "--mysql_user_name",
        required=True,
        help="MySQL user name to use to create the schema",
    )
    parser.add_argument(
        "--mysql_user_password", required=True, help="MySQL user name password"
    )
    parser.add_argument("--ushauri_host", required=True, help="Host name for FormShare")
    parser.add_argument("--ushauri_port", required=True, help="Port for Ushauri")
    args = parser.parse_args()
    ushauri_path = "."

    main_secret = random_password(14).replace("%", "~")
    auth_secret = random_password(14).replace("%", "#")
    auth_secret2 = random_password(14).replace("%", "#")
    aes_key = random_password(29).replace("%", "#")
    auth_opaque = uuid.uuid4().hex

    template_environment = Environment(
        autoescape=False,
        loader=FileSystemLoader(os.path.join(ushauri_path, "templates")),
        trim_blocks=False,
    )
    repository_path = os.path.abspath(args.repository_path)
    context = {
        "mysql_host": args.mysql_host,
        "mysql_port": args.mysql_port,
        "mysql_schema": args.mysql_schema,
        "mysql_user_name": args.mysql_user_name,
        "mysql_user_password": args.mysql_user_password,
        "main_secret": main_secret,
        "auth_secret": auth_secret,
        "auth_secret2": auth_secret2,
        "aes_key": aes_key,
        "auth_opaque": auth_opaque,
        "repository_path": repository_path,
        "odktools_path": args.odktools_path,
        "ushauri_host": args.ushauri_host,
        "ushauri_port": args.ushauri_port,
        "capture_output": args.capture_output,
        "daemon": args.daemon,
        "pid_file": args.pid_file,
        "error_log_file": args.error_log_file,
        "forwarded_allow_ip": args.forwarded_allow_ip,
    }
    rendered_template = template_environment.get_template("ushauri.jinja2").render(
        context
    )

    if not os.path.exists(args.ini_path):
        with open(args.ini_path, "w") as f:
            f.write(rendered_template)
        print("Ushauri INI file created at {}".format(args.ini_path))
    else:
        if args.overwrite:
            with open(args.ini_path, "w") as f:
                f.write(rendered_template)
            print("Ushauri INI file created at {}".format(args.ini_path))
        else:
            print("INI file {} already exists".format(args.ini_path))


if __name__ == "__main__":
    main()
