import argparse
import re

import jsonlines


def save_jsonl(data, path):
    with jsonlines.open(path, "w") as writer:
        writer.write_all(data)

def eval_mbpp(args):
    output = []
    with jsonlines.open(args.input, "r") as reader:
        for line in reader:
            line["correctness"] = []
            code = f"{line['response_text']}\n"
            if "```" in code:
                code = re.search(r"```.*?```", code, re.DOTALL)[0].replace("```", "").strip()
                code += "\n"
            for item in line["test_list"]:
                code_to_run = code + f"{item}\n"
                try:
                    exec(code_to_run)
                    line["correctness"].append("correct")
                except:
                    line["correctness"].append("incorrect")
            line["accuracy"] = sum([1 if x == "correct" else 0 for x in line["correctness"]]) / len(line["correctness"])
            line["total_throughput"] = line["total_tokens"] * 1000 / line["latency"]
            line["completion_thoroughput"] = line["completion_tokens"] * 1000 / line["latency"]
            output.append(line)
    save_jsonl(output, args.output)

def eval_gsm(args):
    output = []
    with jsonlines.open(args.input, "r") as reader:
        for line in reader:
            ref = line["answer"].split("####")[1].strip()
            try:
                hyp = re.search(r"#\d*#", line["response_text"])[0].replace("#", "").strip()
                if ref == hyp:
                    line["correctness"] = "correct"
                else:
                    line["correctness"] = "incorrect"
            except:
                line["correctness"] = "incorrect"
            line["total_throughput"] = line["total_tokens"] * 1000 / line["latency"]
            line["completion_thoroughput"] = line["completion_tokens"] * 1000 / line["latency"]
            output.append(line)
    save_jsonl(output, args.output)

def main(args):
    if args.dataset == "mbpp":
        eval_mbpp(args)
    elif args.dataset == "gsm":
        eval_gsm(args)
    else:
        raise ValueError("Dataset not supported")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()
    main(args)
