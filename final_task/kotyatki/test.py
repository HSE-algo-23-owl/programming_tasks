# Тесты
def test_needleman_wunsch():
    tests = [
        # 1.1.1 Пустые последовательности
        {"id": "1.1.1", "seq1": "", "seq2": "", "match_score": 1, "mismatch_penalty": -1, "gap_penalty": -2, "expected": "Последовательность не должна быть пустой"},
        # 1.2.1 Одна пустая последовательность
        {"id": "1.2.1", "seq1": "AGCT", "seq2": "", "match_score": 1, "mismatch_penalty": -1, "gap_penalty": -2, "expected": "Последовательность не должна быть пустой"},
        {"id": "1.2.1", "seq1": "", "seq2": "AGCT", "match_score": 1, "mismatch_penalty": -1, "gap_penalty": -2, "expected": "Последовательность не должна быть пустой"},
        # 1.1.2 Совпадающие последовательности
        {"id": "1.1.2", "seq1": "AGCT", "seq2": "AGCT", "match_score": 1, "mismatch_penalty": -1, "gap_penalty": -2, "expected": ("AGCT", "AGCT")},
        # 1.1.2 Разные последовательности
        {"id": "1.1.2", "seq1": "AGCT", "seq2": "TCGA", "match_score": 1, "mismatch_penalty": -1, "gap_penalty": -2, "expected": ("AGCT", "TCGA")},
        # 1.1.3 Последовательность 1 не из букв A, G, C, t
        {"id": "1.1.3", "seq1": "XYZ", "seq2": "XYZ", "match_score": 1, "mismatch_penalty": -1, "gap_penalty": -2, "expected": ("XYZ", "XYZ")},
        # 1.2.3 Последовательность 2 не из букв A, G, C, t
        {"id": "1.2.3", "seq1": "AGCT", "seq2": "XYZ", "match_score": 1, "mismatch_penalty": -1, "gap_penalty": -2, "expected": ("AGCT", "-XYZ")},
        # 1.3.4, 1.4.4, 1.5.4 Штрафы не числа
        {"id": "1.3.4", "seq1": "AGCT", "seq2": "TCGA", "match_score": "a", "mismatch_penalty": -1, "gap_penalty": -2, "expected": "Штраф должен быть числом"},
        {"id": "1.4.4", "seq1": "AGCT", "seq2": "TCGA", "match_score": 1, "mismatch_penalty": "b", "gap_penalty": -2, "expected": "Штраф должен быть числом"}]