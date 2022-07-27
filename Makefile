login:
	az account set -s "5763fde3-4253-480c-928f-dfe1e8888a57"
	az configure --defaults workspace="mlw-dev-mlops"  group="rg-dev-mlops"
env:
	az ml environment create --file ./environ/environment.yml
train:
	az ml job create --file ./src/job.yml
