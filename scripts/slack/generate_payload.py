import json
import argparse
import datetime
import re


def get_current_time_string():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def generate_slack_payload(diff_file, output_file, tag_old, tag_new, channel_id):
    try:
        with open(diff_file, 'r') as file:
            diff_content = ''
            for line in file:
                # newline before +++ lines that contain filenames
                diff_content += re.sub(r'\+\+\+', r'\n+++', line)
        # Truncate diff if it's too long for Slack
        max_chars = 39000  # Slack message limit is ~40,000 characters
        if len(diff_content) > max_chars:
            diff_content = diff_content[:max_chars] + '\n... Diff truncated due to size limits ...'

        # Create the payload
        current_time = get_current_time_string()
        payload = {
            'channel': channel_id,
            'text': f'Changes from {tag_old} to {tag_new}, released on {current_time} (UTC):\n{diff_content}'
        }
        with open(output_file, 'w') as json_file:
            json.dump(payload, json_file, indent=2)

        print(f'Slack payload written to {output_file}')
    except Exception as e:
        print(f'Error generating Slack payload: {e}')


def main():
    parser = argparse.ArgumentParser(description='Generate Slack payload JSON file.')
    parser.add_argument('--diff-file', required=True, help='Path to the diff file.')
    parser.add_argument('--output-file', required=True, help='Path to the output JSON file.')
    parser.add_argument('--tag-old', required=True, help='Old tag for the diff.')
    parser.add_argument('--tag-new', required=True, help='New tag for the diff.')
    parser.add_argument('--channel-id', required=True, help='Slack channel ID.')

    args = parser.parse_args()

    generate_slack_payload(
        diff_file=args.diff_file,
        output_file=args.output_file,
        tag_old=args.tag_old,
        tag_new=args.tag_new,
        channel_id=args.channel_id,
    )


if __name__ == '__main__':
    main()
