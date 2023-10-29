def luhn_checksum(imei_str):

    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(imei_str)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return (10 - checksum % 10) % 10

def generate_imeis(base_imei, count):

    base_imei = base_imei[:-1]  # Remove the last digit (checksum)
    generated_imeis = []

    for _ in range(count):
        base_imei = str(int(base_imei) + 1)  # Increment the IMEI
        checksum = luhn_checksum(base_imei)
        new_imei = base_imei + str(checksum)
        generated_imeis.append(new_imei)
    
    # Save generated IMEIs to kaynak.txt
    with open("kaynak.txt", "a") as file:
        for imei in generated_imeis:
            file.write(imei + "\\n")

    return generated_imeis