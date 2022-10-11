# 擬似ターゲット（タスクターゲット）の宣言
.PHONY: set-switch-bot-webhook

all: help

help: ##ヘルプ表示
	@grep -F '##' $(MAKEFILE_LIST) | grep -v grep | sed -e 's/##//g'

init: ##script実行環境の構築
	@docker build ${PWD}/script -t lazy-home-python

set-switch-bot-webhook: ##SwitchBotのWebhookURLを設定
	@docker run -it --rm -v ${PWD}/script:/usr/src/lazy-home/script lazy-home-python python switch_bot/set_up_webhook.py
