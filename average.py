def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def calculate_statistics(numbers):
    if not numbers:
        return None
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    # 중앙값 계산
    if n % 2 == 0:
        median = (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
    else:
        median = sorted_numbers[n // 2]
    
    return {
        "개수": len(numbers),
        "합계": sum(numbers),
        "평균": round(calculate_average(numbers), 2),
        "최대값": max(numbers),
        "최소값": min(numbers),
        "중앙값": round(median, 2)
    }

if __name__ == "__main__":
    try:
        user_input = input("숫자들을 입력하세요 (공백으로 구분): ").strip()
        
        # 입력이 비어있는지 확인
        if not user_input:
            print("⚠️ 숫자를 하나 이상 입력해야 합니다.")
        else:
            # 숫자로 변환
            numbers = list(map(float, user_input.split()))
            
            # 통계 정보 계산 및 출력
            stats = calculate_statistics(numbers)
            print("\n" + "=" * 30)
            print("통계 결과")
            print("=" * 30)
            for key, value in stats.items():
                print(f"{key}: {value}")
            print("=" * 30)
    
    except ValueError:
        print(" 오류: 숫자만 입력할 수 있습니다. 다시 시도하세요.")
    except Exception as e:
        print(f" 예기치 않은 오류가 발생했습니다: {e}")
