OUTPUT_DIR := "./_output"

run-all: clean
	./collect-input.py ../content/zh-cn/docs $(OUTPUT_DIR)

run-all-en: clean
	./collect-input.py ../content/en/docs $(OUTPUT_DIR)

run-admin: clean
	./collect-input.py ../content/zh-cn/docs $(OUTPUT_DIR) admin

run-admin-en: clean
	./collect-input.py ../content/en/docs $(OUTPUT_DIR) admin

run-faq: clean
	./collect-input.py ../content/zh-cn/docs $(OUTPUT_DIR) faq

run-faq-en: clean
	./collect-input.py ../content/en/docs $(OUTPUT_DIR) faq

run-quick: clean
	./collect-input.py ../content/zh-cn/docs $(OUTPUT_DIR) quick

run-quick-en: clean
	./collect-input.py ../content/en/docs $(OUTPUT_DIR) quick

run-quickuse: clean
	./collect-input.py ../content/zh-cn/docs $(OUTPUT_DIR) quickuse

run-quickuse-en: clean
	./collect-input.py ../content/en/docs $(OUTPUT_DIR) quickuse

run-user: clean
	./collect-input.py ../content/zh-cn/docs $(OUTPUT_DIR) user

run-user-en: clean
	./collect-input.py ../content/en/docs $(OUTPUT_DIR) user

clean:
	rm -rf $(OUTPUT_DIR)
