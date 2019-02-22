import numpy as np
import scipy.optimize as optimize
import matplotlib.pyplot as plt

from scipy.integrate import odeint
from sympy import integrate, symbols

# constants (positive)
a = 1
b = 0.5
c = 0.9
d = 2

x01 = 0.8

initial_approx = [0, 0] #Íà÷àëüíîå ïðèáëèæåíèå
end_time = 4.5 #Tk


def system(vars, time):#Èñõîäíàÿ ñèñòåìà ÎÄÓ
 
    x1, x2, Psi1, Psi2 = vars[0], vars[1], vars[2], vars[3]

    dx1dt = x2
    dx2dt = 0.5 * psi2 / a + (d - c * x1)
    dPsi1dt = Psi2 * c
    dPsi2dt = -Psi1
    return dx1dt, dx2dt, dPsi1dt, dPsi2dt


def calculate_ivp(vars):#Ðåøåíèå çàäà÷è Êîøè
    Psi1, Psi2 = vars[0], vars[1]
    time = np.linspace(0, end_time, 100)
    return odeint(system, [x01, 0, Psi1, Psi2], time)


def calculate_final_condition(vars):#Âîçâðàùåíèå ìàññèâà òðàíñâåðñàëüíîñòè è ôóíêöèÿ ôè
    x1, x2, Psi1, Psi2 = vars[0], vars[1], vars[2], vars[3]
    return [Psi1 * b/(x2*x2) - Psi2 * a,  
            a * x1 + b / x2]


def calculate_bvp(vars):#Ðåøåíèå êðàåâîé çàäà÷è
    def subordinate_solution_final_condition(vars):# âîçðàùàåò óðàâíåíèå 
#òðàíñâåðñàëüíîñòè è ôóíêöèþ ôè ñ ïîäñòàâëåííûì ðåøåíèåì çàäà÷è Êîøè
        ivp_solution = calculate_ivp(vars)
        # the last element of the array of solution values is [-1]
        return calculate_final_condition(ivp_solution[-1])

    return optimize.fsolve(subordinate_solution_final_condition, vars)


def calculate_function_g(vars):
    return 1


def calculate_functional(management, time):
    integrand_function = a * management ** 2 + calculate_function_g()
    return integrate(integrand_function, (symbols('t'), 0, time))

#ïîäñòàâëÿåì íà÷àëüíîå ïðèáëèæåíèå
bvp_solution = calculate_bvp(initial_approx)
print('Solution of boundary value problem: %s \n' % bvp_solution)


ivp_solution = calculate_ivp(bvp_solution)
print('Solution of initial value problem: %s \n' % ivp_solution)

# ïðîâåðÿåì ÷òî ðåøåíèå çàäà÷è Êîøè ÿâëÿåþòñÿ íóëÿìè 
check = calculate_final_condition(ivp_solution[-1])
print('Check: %s \n' % check)

time = np.linspace(0, end_time, 100)
x1 = ivp_solution[:, 0]
x2 = ivp_solution[:, 1]
Psi1 = ivp_solution[:, 2]
Psi2 = ivp_solution[:, 3]

management = [] #Ôóíêöèÿ U
for element in Psi2:
    # 4.10
    management.append(element / (2 * a))

x22 = []
for element in x1:
    x22.append(-b / (a * element))


functional = []
for ind in range(len(management)):
    value = calculate_functional(management[ind], end_time, [0, x2[ind]])
    functional.append(value)

min_value = min(functional)
print('Functional: %f' % min_value)

fig = plt.figure()
ax1 = plt.subplot2grid((2, 2), (0, 0))
ax1.plot(time, x1, '-b', label='x1 = x (coordinate)')
ax1.legend(loc='upper left')
ax1.set_xlabel('$t$')
ax1.set_ylabel('$x(t)$')

ax2 = plt.subplot2grid((2, 2), (1, 0))
ax2.plot(time, x2, '-b', label='x2 = v (velocity)')
ax2.legend(loc='upper left')
ax2.set_xlabel('$t$')
ax2.set_ylabel('$v(t)$')

ax3 = plt.subplot2grid((2, 2), (0, 1))
ax3.set_title('optimal management')
ax3.plot(time, management)
ax3.set_xlabel('$t$')
ax3.set_ylabel('$u(t)$')

ax4 = plt.subplot2grid((2, 2), (1, 1))
ax4.set_title('mechanical trajectory of system')
ax4.plot(x1, x2)
ax4.plot(x1, x22, '-b', label='diversity')
ax4.legend(loc='upper left')
ax4.set_xlabel('$x$')
ax4.set_ylabel('$v(x)$')

for ax in fig.axes:
    ax.grid(True)

plt.tight_layout()
plt.show()
