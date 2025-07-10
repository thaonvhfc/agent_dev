import math
import cmath

def solve_cubic(a, b, c, d):
    """
    Solve cubic equation ax³ + bx² + cx + d = 0
    
    Args:
        a, b, c, d: coefficients of the cubic equation
    
    Returns:
        List of roots (real and complex)
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero for a cubic equation")
    
    # Convert to depressed cubic form: t³ + pt + q = 0
    # using substitution x = t - b/(3a)
    p = (3*a*c - b**2) / (3*a**2)
    q = (2*b**3 - 9*a*b*c + 27*a**2*d) / (27*a**3)
    
    # Calculate discriminant
    discriminant = (q/2)**2 + (p/3)**3
    
    roots = []
    
    if discriminant > 0:
        # One real root, two complex conjugate roots
        sqrt_disc = math.sqrt(discriminant)
        u = (-q/2 + sqrt_disc)**(1/3) if (-q/2 + sqrt_disc) >= 0 else -abs(-q/2 + sqrt_disc)**(1/3)
        v = (-q/2 - sqrt_disc)**(1/3) if (-q/2 - sqrt_disc) >= 0 else -abs(-q/2 - sqrt_disc)**(1/3)
        
        # Real root
        t1 = u + v
        x1 = t1 - b/(3*a)
        roots.append(x1)
        
        # Complex roots
        real_part = -(u + v)/2 - b/(3*a)
        imag_part = math.sqrt(3)/2 * (u - v)
        roots.append(complex(real_part, imag_part))
        roots.append(complex(real_part, -imag_part))
        
    elif discriminant == 0:
        # Multiple roots
        if q == 0:
            # Triple root
            x = -b/(3*a)
            roots = [x, x, x]
        else:
            # One single root and one double root
            t1 = 3*q/p
            t2 = -3*q/(2*p)
            x1 = t1 - b/(3*a)
            x2 = t2 - b/(3*a)
            roots = [x1, x2, x2]
    
    else:
        # Three distinct real roots (using trigonometric method)
        r = math.sqrt(-(p/3)**3)
        theta = math.acos(-q/(2*r))
        
        for k in range(3):
            t = 2 * (r**(1/3)) * math.cos((theta + 2*math.pi*k)/3)
            x = t - b/(3*a)
            roots.append(x)
    
    return roots

def format_root(root):
    """Format a root for display"""
    if isinstance(root, complex):
        if abs(root.imag) < 1e-10:
            return f"{root.real:.6f}"
        elif abs(root.real) < 1e-10:
            return f"{root.imag:.6f}i"
        else:
            sign = "+" if root.imag >= 0 else "-"
            return f"{root.real:.6f} {sign} {abs(root.imag):.6f}i"
    else:
        return f"{root:.6f}"

def main():
    """Main function to run the cubic equation solver"""
    print("Cubic Equation Solver")
    print("Solve equations of the form: ax³ + bx² + cx + d = 0")
    print("-" * 50)
    
    try:
        # Get coefficients from user
        a = float(input("Enter coefficient a (x³ term): "))
        b = float(input("Enter coefficient b (x² term): "))
        c = float(input("Enter coefficient c (x term): "))
        d = float(input("Enter coefficient d (constant term): "))
        
        # Solve the equation
        roots = solve_cubic(a, b, c, d)
        
        # Display results
        print(f"\nEquation: {a}x³ + {b}x² + {c}x + {d} = 0")
        print("Roots:")
        for i, root in enumerate(roots, 1):
            print(f"x{i} = {format_root(root)}")
            
        # Verify solutions
        print("\nVerification:")
        for i, root in enumerate(roots, 1):
            if isinstance(root, complex):
                value = a * root**3 + b * root**2 + c * root + d
                print(f"f(x{i}) = {format_root(value)}")
            else:
                value = a * root**3 + b * root**2 + c * root + d
                print(f"f(x{i}) = {value:.10f}")
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
