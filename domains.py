import re
import socket
import smtplib

# 1. Basic syntax validation
def is_valid_syntax(email: str) -> bool:
    # Simple but decent regex for basic email syntax
    pattern = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
    return re.match(pattern, email) is not None


# 2. Find a host that *might* accept SMTP on port 25 (no external DNS package)
def find_smtp_host(domain: str, timeout: int = 5) -> str | None:
    candidates = [
        domain,
        f"mail.{domain}",
        f"smtp.{domain}",
    ]

    for host in candidates:
        try:
            # If this resolves and has an IP for port 25, we assume it's worth trying
            print(f"trying host: {host}")
            socket.getaddrinfo(host, 25)
            return host
        except socket.gaierror:
            continue

    return None


# 3. Try SMTP "RCPT TO" without actually sending an email
def verify_email_smtp(
    email: str,
    from_address: str = "gauvij.99@gmail.com",
    timeout: int = 10,
) -> tuple[bool, str]:
    """
    Returns (is_probably_deliverable, explanation)
    Uses only Python stdlib: re, socket, smtplib.
    """

    print(f"Verifying email: {email}")

    print(f"Checking syntax...")

    # Step 1: Syntax
    if not is_valid_syntax(email):
        return False, "Invalid email syntax"

    local_part, domain = email.rsplit("@", 1)

    print(f"Finding SMTP HOST...")

    # Step 2: Check domain resolves + guess an SMTP host
    smtp_host = find_smtp_host(domain, timeout=timeout)
    if not smtp_host:
        return False, "Could not find an SMTP server for this domain"
    
    print(f"Using the SMTP host: {smtp_host}")

    try:
        # Step 3: SMTP conversation
        with smtplib.SMTP(smtp_host, 25, timeout=timeout) as server:
            # You may need server.starttls() for some hosts, but many block direct TLS-less access.
            server.helo("gmail.com")

            # MAIL FROM (fake address just for testing)
            server.mail(from_address)

            # RCPT TO – the crucial step
            code, message = server.rcpt(email)

            # 250/251 usually means “OK”
            if code in (250, 251):
                return True, f"Server accepted RCPT TO. Code: {code}, Message: {message.decode(errors='ignore')}"
            else:
                return False, f"Server rejected RCPT TO. Code: {code}, Message: {message.decode(errors='ignore')}"

    except (socket.error, smtplib.SMTPException) as e:
        return False, f"SMTP error: {e}"


# Example usage
if __name__ == "__main__":
    test_email = "gvofficial99@gmail.com"
    ok, info = verify_email_smtp(test_email)
    print(test_email, "->", ok, "|", info)
