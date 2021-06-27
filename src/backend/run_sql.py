import subprocess


def run(sql, user="root", password="admin"):
    """
    RUNS SQL COMMANDS AND RETURNS RAW OUTPUT
    :param sql:
    :param user:
    :param password:
    :return:
    """
    command = ["mysql", "-u", user, f"-p{password}", "-vvv", "--table", "-e", sql]
    s = subprocess.run(command, capture_output=True, text=True)
    if "error" in str(s.stderr.lower()):
        print(s.stderr)
        raise Exception("YOUR SQL SYNTAX HAS AN ERROR!")
    else:
        return str(s.stdout)


def get_output(sql, user="root", password="admin"):
    """
    RUNS SQL COMMAND AND MATCHES EACH COMMAND WITH ITS OUTPUT
    :param sql:
    :param user:
    :param password:
    :return:
    """
    output_list = run(sql, user, password).split("\n")
    separator = "--------------"
    expected_end = 0
    query, q_output, parsed_output = [], [], []
    for i in range(len(output_list)):
        line = output_list[i]
        if line == separator and not expected_end:
            expected_end = 1
        elif line == separator and expected_end == 1:
            expected_end = 2
        elif line == separator and expected_end == 2:
            parsed_output.append(("\n".join(query), "\n".join(q_output)))
            query, q_output = [], []
            expected_end = 1
        elif i+1 == len(output_list):
            parsed_output.append(("\n".join(query), "\n".join(q_output)))
        elif expected_end == 1:
            query.append(line)
        elif expected_end == 2:
            q_output.append(line)
    return parsed_output


def group_sql_output(original_query, user="root", password="admin"):
    """
    GROUPS CONSECUTIVE SQL COMMANDS WITH NO OUTPUT IN PARSED OUTPUT LIST
    :param original_query:
    :param user:
    :param password:
    :return:
    """
    output_list = get_output(original_query, user=user, password=password)
    grouped_output = []
    cursor = 0
    for entry in output_list:
        query_with_out, query_output = entry[0], entry[1]
        new_cursor = original_query.find(query_with_out) + len(query_with_out) + 1
        grouped_output.append((original_query[cursor:new_cursor], query_output))
        cursor = new_cursor
    return grouped_output
