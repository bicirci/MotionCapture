
import math
import struct

#for storing
#theta =  asin( 2.0f * q.w * q.y - 2.0f * q.x * q.z ); pitch
#phi   = atan2( 2.0f * q.w * q.x + 2.0f * q.y * q.z, 1.0f - 2.0f * q.x * q.x - 2.0f * q.y * q.y ); yaw
#psi   = atan2( 2.0f * q.w * q.z + 2.0f * q.x * q.y, 1.0f - 2.0f * q.y * q.y - 2.0f * q.z * q.z ); roll



class sensor_tag:
    def __init__(self):
        self.q0 = 1
        self.q1 = 0
        self.q2 = 0
        self.q3 = 0

    def updateQuats(self,q0, q1, q2, q3):
        self.q0 = q0
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3

    def getQuats(self):
        return self.q0, self.q1,self.q2,self.q3
#sampleFreq = 512.0   # made not global

betaDef = 0.00
beta =  betaDef

#q0 = 1.0
#q1 = 0.0
#q2 = 0.0
#q3 = 0.0

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


def MadgwickAHRSupdate(gx, gy, gz, ax, ay, az, mx, my, mz, sampleFreq, q0, q1, q2, q3):
    #global sampleFreq
    global betaDef
    #global q0, q1, q2, q3
    global beta

	#Rate of change of quaternion from gyroscope
    qDot1 = 0.5 * (-q1 * gx - q2 * gy - q3 * gz)
    qDot2 = 0.5 * (q0 * gx + q2 * gz - q3 * gy)
    qDot3 = 0.5 * (q0 * gy - q1 * gz + q3 * gx)
    qDot4 = 0.5 * (q0 * gz + q1 * gy - q2 * gx)

	#Compute feedback only if accelerometer measurement valid (avoids NaN in accelerometer normalisation)
    if (ax != 0.0) and (ay != 0.0) and (az != 0.0) :

		#Normalise accelerometer measurement
        recipNorm = invSqrt(ax * ax + ay * ay + az * az)
        ax *= recipNorm
        ay *= recipNorm
        az *= recipNorm

		#Normalise magnetometer measurement
        recipNorm = invSqrt(mx * mx + my * my + mz * mz)
        mx *= recipNorm
        my *= recipNorm
        mz *= recipNorm

		#Auxiliary variables to avoid repeated arithmetic
        _2q0mx = 2.0 * q0 * mx
        _2q0my = 2.0 * q0 * my
        _2q0mz = 2.0 * q0 * mz
        _2q1mx = 2.0 * q1 * mx
        _2q0 = 2.0 * q0
        _2q1 = 2.0 * q1
        _2q2 = 2.0 * q2
        _2q3 = 2.0 * q3
        _2q0q2 = 2.0 * q0 * q2
        _2q2q3 = 2.0 * q2 * q3
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

		#Reference direction of Earth's magnetic field
        hx = mx * q0q0 - _2q0my * q3 + _2q0mz * q2 + mx * q1q1 + _2q1 * my * q2 + _2q1 * mz * q3 - mx * q2q2 - mx * q3q3
        hy = _2q0mx * q3 + my * q0q0 - _2q0mz * q1 + _2q1mx * q2 - my * q1q1 + my * q2q2 + _2q2 * mz * q3 - my * q3q3
        _2bx = math.sqrt(hx * hx + hy * hy)
        _2bz = -_2q0mx * q2 + _2q0my * q1 + mz * q0q0 + _2q1mx * q3 - mz * q1q1 + _2q2 * my * q3 - mz * q2q2 + mz * q3q3
        _4bx = 2.0 * _2bx
        _4bz = 2.0 * _2bz

		#Gradient decent algorithm corrective step
        s0 = -_2q2 * (2.0 * q1q3 - _2q0q2 - ax) + _2q1 * (2.0 * q0q1 + _2q2q3 - ay) - _2bz * q2 * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (-_2bx * q3 + _2bz * q1) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + _2bx * q2 * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
        s1 = _2q3 * (2.0 * q1q3 - _2q0q2 - ax) + _2q0 * (2.0 * q0q1 + _2q2q3 - ay) - 4.0 * q1 * (1 - 2.0 * q1q1 - 2.0 * q2q2 - az) + _2bz * q3 * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (_2bx * q2 + _2bz * q0) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + (_2bx * q3 - _4bz * q1) * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
        s2 = -_2q0 * (2.0 * q1q3 - _2q0q2 - ax) + _2q3 * (2.0 * q0q1 + _2q2q3 - ay) - 4.0 * q2 * (1 - 2.0 * q1q1 - 2.0 * q2q2 - az) + (-_4bx * q2 - _2bz * q0) * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (_2bx * q1 + _2bz * q3) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + (_2bx * q0 - _4bz * q2) * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
        s3 = _2q1 * (2.0 * q1q3 - _2q0q2 - ax) + _2q2 * (2.0 * q0q1 + _2q2q3 - ay) + (-_4bx * q3 + _2bz * q1) * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (-_2bx * q0 + _2bz * q2) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + _2bx * q1 * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
        recipNorm = invSqrt(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3) #normalise step magnitude
        s0 *= recipNorm
        s1 *= recipNorm
        s2 *= recipNorm
        s3 *= recipNorm

		#Apply feedback step
        qDot1 -= beta * s0
        qDot2 -= beta * s1
        qDot3 -= beta * s2
        qDot4 -= beta * s3


	#Integrate rate of change of quaternion to yield quaternion
    q0 += qDot1 * (1.0 / sampleFreq)
    q1 += qDot2 * (1.0 / sampleFreq)
    q2 += qDot3 * (1.0 / sampleFreq)
    q3 += qDot4 * (1.0 / sampleFreq)

	#Normalise quaternion
    recipNorm = invSqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3)
    q0 *= recipNorm
    q1 *= recipNorm
    q2 *= recipNorm
    q3 *= recipNorm

    return q0, q1, q2, q3

#MadgwickAHRSupdate(-23.98, 3.51, -6.71, 4.03, 7.34, -3.96, -16706, -16706,-16706)
#print(str(q0) + ", " + str(q1) + ", " + str(q2) + ", " + str(q3))
#MadgwickAHRSupdate(-15.29, 2.92, -1.05, 4.45, 7.64, -4.59, 450, 569, 50)
#MadgwickAHRSupdate(2.32, -1.37, -2.13,2.34, 10.57, -0.76, -518, -482,-101)
#print(str(q0) + ", " + str(q1) + ", " + str(q2) + ", " + str(q3))
