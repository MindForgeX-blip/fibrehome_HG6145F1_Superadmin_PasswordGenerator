import hashlib
import re

UPPER = 'ACDFGHJMNPRSTUWXY'
LOWER = 'abcdfghjkmpstuwxy'
DIGIT = '2345679'
SYMBOL = '!@$&%'

def _mod(v, m):
    '''C-style modulo handling for negative values'''
    return v % m

def mac_to_pass(mac: str) -> str:
    '''Generate Fiberhome HG6145F1 admin password from MAC address'''
    # Validate MAC format (XX:XX:XX:XX:XX:XX)
    if not re.fullmatch('([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', mac):
        return 'Invalid MAC format (expected XX:XX:XX:XX:XX:XX)'
    
    # Create MD5 hash of MAC + salt
    md5 = hashlib.md5()
    md5.update(mac.encode())        # Add MAC address
    md5.update(b'AEJLY')            # Add salt "AEJLY"
    digest = md5.hexdigest()        # Get hex digest
    
    # Convert hex characters to numeric values
    vals = []
    for c in digest[:20]:           # Use first 20 characters of hash
        if '0' <= c <= '9':
            vals.append(ord(c) - ord('0'))
        elif 'a' <= c <= 'f':
            vals.append(ord(c) - ord('a') + 10)
        elif 'A' <= c <= 'F':
            vals.append(ord(c) - ord('A') + 10)
        else:
            vals.append(0)          # Fallback (should not happen with hex)
    
    # Initialize password array (16 characters)
    password = [''] * 16
    
    # Generate password characters
    for i in range(16):
        v = vals[i]
        sel = _mod(v, 4)  # Determine character set (0-3)
        
        if sel == 0:  # UPPER case letters
            password[i] = UPPER[v * 2 % 17]
        elif sel == 1:  # LOWER case letters
            password[i] = LOWER[(v * 2 + 1) % 17]
        elif sel == 2:  # DIGITS
            password[i] = DIGIT[6 - v % 7]
        elif sel == 3:  # SYMBOLS
            password[i] = SYMBOL[4 - v % 5]
    
    # Calculate special positions for character set representatives
    p0 = _mod(vals[16] + 1, 16)
    p1 = _mod(vals[17] + 1, 16)
    p2 = _mod(vals[18] + 1, 16)
    p3 = _mod(vals[19] + 1, 16)
    
    # Ensure all positions are unique
    used = set()
    positions = [p0, p1, p2, p3]
    
    for i in range(len(positions)):
        while positions[i] in used:
            positions[i] = _mod(positions[i] + 1, 16)
        used.add(positions[i])
    
    # Insert character set representatives at calculated positions
    password[positions[0]] = UPPER[(vals[16] * 2) % 17]
    password[positions[1]] = LOWER[((vals[17] * 2) + 1) % 17]
    password[positions[2]] = DIGIT[6 - (vals[18] % 7)]
    password[positions[3]] = SYMBOL[4 - (vals[19] % 5)]
    
    return ''.join(password)

def main():
    print("=" * 60)
    print("Fiberhome HG6145F1 Admin Password Generator")
    print("By MindForgeX-blip on github")
    print("=" * 60)
    print()
    
    while True:
        print("Enter MAC address (format: XX:XX:XX:XX:XX:XX)")
        print("Or type 'quit' to exit")
        print("-" * 40)
        
        mac = input("MAC: ").strip()
        
        if mac.lower() == 'quit':
            print("Goodbye!")
            break
        
        result = mac_to_pass(mac.upper())
        print("\n" + "=" * 40)
        print(f"Input MAC: {mac.upper()}")
        print(f"Generated Password: {result}")
        print("=" * 40 + "\n")
        
        # Ask if user wants to continue
        again = input("Generate another? (y/n): ").strip().lower()
        if again != 'y':
            print("Goodbye!")
            break
        print()

if __name__ == '__main__':
    main()
