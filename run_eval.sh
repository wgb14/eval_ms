#!/bin/bash

# Run evaluation
if [[ $# -ne 3 ]]; then
    echo "Usage: run_eval.sh [model_name] [input_path] [output_path]"
    exit 1
fi

model_name=$1
input_path=`realpath $2`
output_path=`realpath $3`

echo "evaluating ${model_name} on mbpp..."
input_mbpp=${input_path}/mbpp_${model_name}.json
output_mbpp=${output_path}/eval_mbpp_${model_name}.json
echo "input: ${input_mbpp}, output: ${output_mbpp}"
if [[ ! -f ${input_mbpp} ]]; then
    echo "input file ${input_mbpp} does not exist"
    exit 1
fi
python eval_ms.py --input ${input_mbpp} --output ${output_mbpp} --dataset mbpp
echo done

echo "evaluating ${model_name} on gsm..."
input_gsm=${input_path}/gsm_${model_name}.json
output_gsm=${output_path}/eval_gsm_${model_name}.json
echo "input: ${input_gsm}, output: ${output_gsm}"
if [[ ! -f ${input_gsm} ]]; then
    echo "input file ${input_gsm} does not exist"
    exit 1
fi
python eval_ms.py --input ${input_gsm} --output ${output_gsm} --dataset gsm
echo done
