def get_auth_html():
    return """
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-header">
                <div class="lock-animation">
                    <div class="lock-body">
                        <div class="keyhole"></div>
                    </div>
                    <div class="lock-glow"></div>
                </div>
                <h1>Welcome to VaultX</h1>
                <p>Secure Data Locker</p>
            </div>
            <div class="mode-switcher">
                <button class="mode-btn active" data-mode="login">Login</button>
                <button class="mode-btn" data-mode="register">Register</button>
            </div>
            <form id="authForm">
                <div class="form-group">
                    <input type="text" id="username" placeholder="Username" required>
                    <div class="input-glow"></div>
                </div>
                <div class="form-group">
                    <input type="password" id="password" placeholder="Password" required>
                    <div class="input-glow"></div>
                </div>
                <div class="form-group register-only">
                    <input type="password" id="confirmPassword" placeholder="Confirm Password">
                    <div class="input-glow"></div>
                </div>
                <div class="form-group register-only">
                    <input type="email" id="email" placeholder="Email Address">
                    <div class="input-glow"></div>
                </div>
                <div class="error-message"></div>
                <button type="submit" class="submit-btn">
                    <span class="btn-text">Login</span>
                    <div class="btn-glow"></div>
                </button>
            </form>
        </div>
    </div>

    <style>
    /* Center all content */
    .auth-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100vw;
        height: 100vh;
        background: linear-gradient(135deg, rgba(2,6,23,0.95), rgba(15,23,42,0.95));
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1;
    }

    /* Centered card with improved alignment */
    .auth-card {
        width: 90%;
        max-width: 400px;
        background: rgba(15, 23, 42, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 0 40px rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(59, 130, 246, 0.2);
        animation: cardFloat 0.5s ease-out;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    /* Enhanced centered header styling */
    .auth-header {
        width: 100%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        margin-bottom: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .auth-header h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
        background: linear-gradient(to right, #60A5FA, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-shadow: 0 0 20px rgba(96, 165, 250, 0.5);
        animation: fadeInDown 0.8s ease-out;
    }

    .auth-header p {
        font-size: 1.2rem;
        color: #94A3B8;
        text-align: center;
        animation: fadeInUp 0.8s ease-out;
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Center mode switcher */
    .mode-switcher {
        width: 100%;
        max-width: 320px;
        margin: 0 auto 2rem;
        display: flex;
        justify-content: center;
        gap: 1rem;
    }

    .mode-btn {
        flex: 1;
        padding: 0.75rem;
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 10px;
        background: rgba(15, 23, 42, 0.95);
        color: #E2E8F0;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .mode-btn.active {
        background: rgba(59, 130, 246, 0.2);
        border-color: #3B82F6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
    }

    /* Ensure form contents are centered */
    #authForm {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
    }

    .form-group {
        width: 100%;
        max-width: 320px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .form-group input {
        width: 100%;
        padding: 1rem;
        background: rgba(15, 23, 42, 0.95);
        border: 2px solid rgba(59, 130, 246, 0.3);
        border-radius: 10px;
        color: #E2E8F0;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .form-group input:focus {
        outline: none;
        border-color: #3B82F6;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
    }

    .input-glow {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 10px;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .form-group input:focus + .input-glow {
        opacity: 1;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
    }

    .register-only {
        display: none;
    }

    .error-message {
        color: #EF4444;
        text-align: center;
        margin: 1rem 0;
        min-height: 20px;
        font-size: 0.875rem;
    }

    /* Center submit button */
    .submit-btn {
        width: 100%;
        max-width: 320px;
        margin: 1rem auto;
        padding: 1rem;
        background: linear-gradient(45deg, #2563EB, #3B82F6);
        border: none;
        border-radius: 10px;
        color: white;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .submit-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
    }

    .btn-glow {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.2), transparent);
        transform: translateX(-100%);
        transition: transform 0.5s ease;
    }

    .submit-btn:hover .btn-glow {
        transform: translateX(100%);
    }

    @keyframes cardFloat {
        from { 
            opacity: 0; 
            transform: translate(-50%, -40%);
        }
        to { 
            opacity: 1; 
            transform: translate(-50%, -50%);
        }
    }

    @keyframes lockPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }

    @keyframes glowPulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 0.8; }
    }
    </style>

    <script>
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const isRegister = btn.dataset.mode === 'register';
            document.querySelectorAll('.register-only').forEach(el => {
                el.style.display = isRegister ? 'block' : 'none';
            });
            
            document.querySelector('.submit-btn .btn-text').textContent = 
                isRegister ? 'Register' : 'Login';
        });
    });

    document.getElementById('authForm').addEventListener('submit', (e) => {
        e.preventDefault();
        // Your existing form submission logic
    });
    </script>
    """