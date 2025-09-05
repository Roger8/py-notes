#coding:utf-8
# 椭圆求解

import numpy as np
import matplotlib.pyplot as plt

def generate_ellipse_points(center, axes, angle, num_points=100, noise=0.5):
    t = np.linspace(0, 2 * np.pi, num_points)
    x = axes[0] * np.cos(t)
    y = axes[1] * np.sin(t)
    # 旋转
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    pts = np.dot(R, np.vstack((x, y)))
    pts[0] += center[0]
    pts[1] += center[1]
    pts += np.random.normal(scale=noise, size=pts.shape)
    return pts.T

def fit_ellipse(points):
    x = points[:, 0]
    y = points[:, 1]
    D = np.vstack([x**2, x*y, y**2, x, y, np.ones_like(x)]).T
    S = np.dot(D.T, D)
    print("S:",S)
    _, _, V = np.linalg.svd(S)
    print("V:",V)
    params = V[-1, :]
    print("params:",params)
    print("-"*30)
    return params

def ellipse_parameters(params):
    A, B, C, D, E, F = params
    den = B**2 - 4*A*C
    if den == 0:
        raise ValueError("Denominator zero, not an ellipse.")
    x0 = (2*C*D - B*E) / den
    y0 = (2*A*E - B*D) / den

    # 旋转角
    if B == 0 and A < C:
        theta = 0
    elif B == 0 and A >= C:
        theta = np.pi/2
    else:
        theta = 0.5 * np.arctan2(B, A - C)

    # 计算长短轴
    up = 2*(A*E**2 + C*D**2 + F*B**2 - 2*B*D*E - A*C*F)
    down1 = (B**2 - 4*A*C) * ((A + C) + np.sqrt((A - C)**2 + B**2))
    down2 = (B**2 - 4*A*C) * ((A + C) - np.sqrt((A - C)**2 + B**2))
    a = np.sqrt(abs(up / down1))
    b = np.sqrt(abs(up / down2))

    return (x0, y0), a, b, theta

def plot_ellipse(center, a, b, theta, ax, **kwargs):
    t = np.linspace(0, 2 * np.pi, 200)
    x = a * np.cos(t)
    y = b * np.sin(t)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    pts = np.dot(R, np.vstack((x, y)))
    pts[0] += center[0]
    pts[1] += center[1]
    ax.plot(pts[0], pts[1], **kwargs)

# 示例：生成并拟合3组椭圆
np.random.seed(42)
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

for i, ax in enumerate(axs):
    # 随机参数
    center = np.random.uniform(-10, 10, 2)
    axes = np.random.uniform(2, 6, 2)
    angle = np.random.uniform(0, np.pi)
    points = generate_ellipse_points(center, axes, angle, num_points=5, noise=0.01)
    params = fit_ellipse(points)
    try:
        fit_center, a, b, fit_angle = ellipse_parameters(params)
        ax.scatter(points[:, 0], points[:, 1], s=10, label='Points')
        plot_ellipse(fit_center, a, b, fit_angle, ax, color='r', label='Fitted Ellipse')
        plot_ellipse(center, axes[0], axes[1], angle, ax, color='g', linestyle='--', label='True Ellipse')
        ax.set_title(f"Ellipse {i+1}\nCenter: {fit_center}\nAxes: ({a:.2f}, {b:.2f})\nAngle: {np.degrees(fit_angle):.1f}°")
        ax.axis('equal')
        ax.legend()
    except Exception as e:
        ax.set_title(f"Fit failed: {e}")

plt.tight_layout()
plt.show()
