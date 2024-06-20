def initialize_matrix(rows, columns):
    return [[0] * columns for _ in range(rows)]


def needleman_wunsch(seq1, seq2, match=2, mismatch=-1, gap=-1):
    if not isinstance(match, (int, float)) or not isinstance(mismatch, (int, float)) or not isinstance(gap,
                                                                                                       (int, float)):
        raise ValueError("Штраф должен быть числом")
    if not seq1 and not seq2:
        raise ValueError("Последовательность не должна быть пустой")
    if not seq1 or not seq2:
        raise ValueError("Последовательность не должна быть пустой")

    matrix = initialize_matrix(len(seq1) + 1, len(seq2) + 1)

    for i in range(1, len(seq1) + 1):
        matrix[i][0] = matrix[i - 1][0] + gap

    for j in range(1, len(seq2) + 1):
        matrix[0][j] = matrix[0][j - 1] + gap

    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            if seq1[i - 1] == seq2[j - 1]:
                match_score = matrix[i - 1][j - 1] + match
            else:
                match_score = matrix[i - 1][j - 1] + mismatch

            score1 = matrix[i - 1][j] + gap
            score2 = matrix[i][j - 1] + gap
            matrix[i][j] = max(match_score, score1, score2)
    return matrix


def traceback(seq1, seq2, matrix, match=2, mismatch=-1, gap=-1):
    aligned_seq1 = ''
    aligned_seq2 = ''
    i = len(seq1)
    j = len(seq2)
    while i > 0 and j > 0:
        if i > 0 and j > 0 and matrix[i][j] == matrix[i - 1][j - 1] + (
        match if seq1[i - 1] == seq2[j - 1] else mismatch):
            aligned_seq1 += seq1[i - 1]
            aligned_seq2 += seq2[j - 1]
            i -= 1
            j -= 1
        elif i > 0 and matrix[i][j] == matrix[i - 1][j] + gap:
            aligned_seq1 += seq1[i - 1]
            aligned_seq2 += '-'
            i -= 1
        else:
            aligned_seq1 += '-'
            aligned_seq2 += seq2[j - 1]
            j -= 1
    while i > 0:
        aligned_seq1 += seq1[i - 1]
        aligned_seq2 += '-'
        i -= 1
    while j > 0:
        aligned_seq1 += '-'
        aligned_seq2 += seq2[j - 1]
        j -= 1
    return aligned_seq1[::-1], aligned_seq2[::-1]
