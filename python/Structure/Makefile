PYTHON = PYTHONPATH=. python3

.PHONY: run_multiplos run_fibonacci run_factor_primo test help install

run_multiplos:
	@read -p "Ingresa n: " N; \
	read -p "Ingresa x: " X; \
	read -p "Ingresa y: " Y; \
	PYTHONPATH=. python3 problemas/multiplos.py --n=$$N --x=$$X --y=$$Y

run_fibonacci:
	@read -p "Ingresa N (dejar vacío para usar lista interna): " N; \
	if [ -n "$$N" ]; then \
		PYTHONPATH=. python3 problemas/fibonacci.py --n=$$N; \
	else \
		PYTHONPATH=. python3 problemas/fibonacci.py; \
	fi

run_factor_primo:
	@read -p "Ingresa N (dejar vacío para usar lista interna): " N; \
	if [ -n "$$N" ]; then \
		PYTHONPATH=. python3 problemas/factor_primo.py --n=$$N; \
	else \
		PYTHONPATH=. python3 problemas/factor_primo.py; \
	fi

test:
	$(PYTHON) tests/tests_operaciones.py
	$(PYTHON) tests/test_decorador.py
	$(PYTHON) tests/test_multiplos.py
	$(PYTHON) tests/test_fibonacci.py
	$(PYTHON) tests/test_factor_primo.py

help:
	@echo "=== multiplos.py ==="
	@$(PYTHON) problemas/multiplos.py --help
	@echo ""
	@echo "=== fibonacci.py ==="
	@$(PYTHON) problemas/fibonacci.py --help
	@echo ""
	@echo "=== factor_primo.py ==="
	@$(PYTHON) problemas/factor_primo.py --help

install:
	pip install -r requirements.txt
