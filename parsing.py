import os
import re
import json

# Because some of the tag is missing,  

ROOT = '/Users/Constance/Spring2016/text_mining/project'
END_TAG = "X-FileName"


def parsing_file(file_name):
    print("parsing:" + file_name)
    output = {}
    s = open(file_name).read().split('\r\n')
    tag_list = ["Message-ID", "Date", "From", "To", "Subject", "Mime-Version", "Content-Type", "Content-Transfer-Encoding", "X-From", "X-To", "X-cc", "X-bcc", "X-Folder", "X-Origin", "X-FileName"]

    l_number = 0

    for i, tag in enumerate(tag_list):
        if l_number == len(s):
            # reaching EOF but has not finished the tags.
            return None
        tag_value = ""
        if i == len(tag_list) - 1:
            tag_value += s[l_number][len(tag) + 2:]
            l_number += 1
        else:
            next_tag = tag_list[i + 1]
            while True:
                if l_number == len(s):
                    # reaching EOF but has not finished the tags.
                    return None
                if s[l_number][:len(next_tag)] == next_tag:
                    break
                if s[l_number][:len(tag)] == tag:
                    tag_value += s[l_number][len(tag)+2:]
                else:
                    tag_value += s[l_number]
                l_number += 1
        output[tag] = tag_value

    output["Content"] = "\n".join(s[l_number:])

    pattern = re.compile('forwarded')
    output["Forward Times"] = len(pattern.findall(output["Content"].lower()))

    return output

def iter_files():
    valid_count = 0
    invalid_count = 0
    for name in os.listdir(os.path.join(ROOT, 'maildir/')):
        email_list = []
        for email_dir in os.listdir(os.path.join(ROOT, 'maildir/', name)):
            for root, dirs, files in os.walk(os.path.join(ROOT, 'maildir/', name, email_dir)):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    email = parsing_file(file_path)
                    if email is None:
                        invalid_count += 1
                        continue
                    valid_count += 1
                    email["Name Directory"] = name
                    email["Email Directory"] = email_dir
                    email_list.append(email)
        json.dump(email_list, open(os.path.join(ROOT, 'enron_output/', name + '.json'), 'w'), ensure_ascii=False) 
    print("valid count: " + str(valid_count))
    print("invalid count: " + str(invalid_count))

if __name__ == "__main__":
    iter_files()
