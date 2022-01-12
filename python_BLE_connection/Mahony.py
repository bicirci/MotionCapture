
import math
import struct

# from http://ajcr.net/fast-inverse-square-root-python/
def invSqrt(number):
    threehalfs = 1.5
    x2 = number * 0.5
    y = number

    packed_y = struct.pack('f', y)
    i = struct.unpack('i', packed_y)[0]  # treat float's bytes as int
    i = 0x5f3759df - (i >> 1)            # arithmetic with magic number
    packed_i = struct.pack('i', i)
    y = struct.unpack('f', packed_i)[0]  # treat int's bytes as float

    y = y * (threehalfs - (x2 * y * y))  # Newton's method
    return y

#---------------------------------------------------------------------------------------------------
# Definitions

#sampleFreq = 512.0    #sample frequency in Hz
twoKpDef = 2.0 * 1.75    #2 * proportional gain
twoKiDef = 2.0 * 0.05    #2 * integral gain

#---------------------------------------------------------------------------------------------------
# Variable definitions

twoKp = twoKpDef										# 2 * proportional gain (Kp)
twoKi = twoKiDef									# 2 * integral gain (Ki)
q0 = 1.0
q1 = 0.0
q2 = 0.0
q3 = 0.0					# quaternion of sensor frame relative to auxiliary frame
integralFBx = 0.0
integralFBy = 0.0
integralFBz = 0.0	# integral error terms scaled by Ki


#====================================================================================================
# Functions

#---------------------------------------------------------------------------------------------------
# AHRS algorithm update

def MahonyAHRSupdate(gx, gy, gz, ax, ay, az, mx, my, mz, sampleFreq):
    global twoKiDef, twoKiDef
    global q0, q1, q2, q3
    global twoKp, twoKi
    global integralFBx, integralFBy, integralFBz


	# Compute feedback only if accelerometer measurement valid (avoids NaN in accelerometer normalisation)
    if (ax != 0.0) and (ay != 0.0) and (az != 0.0) :

		# Normalise accelerometer measurement
        recipNorm = invSqrt(ax * ax + ay * ay + az * az)
        ax *= recipNorm
        ay *= recipNorm
        az *= recipNorm

		# Normalise magnetometer measurement
        recipNorm = invSqrt(mx * mx + my * my + mz * mz)
        mx *= recipNorm
        my *= recipNorm
        mz *= recipNorm

        # Auxiliary variables to avoid repeated arithmetic
        q0q0 = q0 * q0
        q0q1 = q0 * q1
        q0q2 = q0 * q2
        q0q3 = q0 * q3
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q3q3 = q3 * q3

        # Reference direction of Earth's magnetic field
        hx = 2.0 * (mx * (0.5 - q2q2 - q3q3) + my * (q1q2 - q0q3) + mz * (q1q3 + q0q2))
        hy = 2.0 * (mx * (q1q2 + q0q3) + my * (0.5 - q1q1 - q3q3) + mz * (q2q3 - q0q1))
        bx = math.sqrt(hx * hx + hy * hy)
        bz = 2.0 * (mx * (q1q3 - q0q2) + my * (q2q3 + q0q1) + mz * (0.5 - q1q1 - q2q2))

		# Estimated direction of gravity and magnetic field
        halfvx = q1q3 - q0q2
        halfvy = q0q1 + q2q3
        halfvz = q0q0 - 0.5 + q3q3
        halfwx = bx * (0.5 - q2q2 - q3q3) + bz * (q1q3 - q0q2)
        halfwy = bx * (q1q2 - q0q3) + bz * (q0q1 + q2q3)
        halfwz = bx * (q0q2 + q1q3) + bz * (0.5 - q1q1 - q2q2)

		# Error is sum of cross product between estimated direction and measured direction of field vectors
        halfex = (ay * halfvz - az * halfvy) + (my * halfwz - mz * halfwy)
        halfey = (az * halfvx - ax * halfvz) + (mz * halfwx - mx * halfwz)
        halfez = (ax * halfvy - ay * halfvx) + (mx * halfwy - my * halfwx)

		# Compute and apply integral feedback if enabled
        if (twoKi > 0.0):
            integralFBx += twoKi * halfex * (1.0 / sampleFreq)	# integral error scaled by Ki
            integralFBy += twoKi * halfey * (1.0 / sampleFreq)
            integralFBz += twoKi * halfez * (1.0 / sampleFreq)
            gx += integralFBx	# apply integral feedback
            gy += integralFBy
            gz += integralFBz
        else:
            integralFBx = 0.0	# prevent integral windup
            integralFBy = 0.0
            integralFBz = 0.0

		# Apply proportional feedback
        gx += twoKp * halfex
        gy += twoKp * halfey
        gz += twoKp * halfez


	# Integrate rate of change of quaternion
    gx *= (0.5 * (1.0 / sampleFreq))		# pre-multiply common factors
    gy *= (0.5 * (1.0 / sampleFreq))
    gz *= (0.5 * (1.0 / sampleFreq))
    qa = q0
    qb = q1
    qc = q2
    q0 += (-qb * gx - qc * gy - q3 * gz)
    q1 += (qa * gx + qc * gz - q3 * gy)
    q2 += (qa * gy - qb * gz + q3 * gx)
    q3 += (qa * gz + qb * gy - qc * gx)

	# Normalise quaternion
    recipNorm = invSqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3)
    q0 *= recipNorm
    q1 *= recipNorm
    q2 *= recipNorm
    q3 *= recipNorm

    return q0, q1, q2, q3

#====================================================================================================
# END OF CODE
#====================================================================================================
