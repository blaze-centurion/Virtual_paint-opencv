import cv2
import numpy as np

cap = cv2.VideoCapture(0)
width = 640
height = 480
cap.set(3, width)
cap.set(4, height)
cap.set(10, 150)

myColors = [
			[0, 165, 70, 18, 255, 255],  ## orange
			[132, 63, 0, 255, 255, 255], ## pink
 			[107, 123, 2, 255, 255, 255]  ## blue
			]
myColorsValue = [
				[12,82,245],
				[151, 0, 252],
				[255, 0, 0]
				]

myPoints =  [] #[x, y, ColorId] 


def findColor(img, myColors, myColorsValue):  
	imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	# lower = np.array([h_min, s_min, v_min])
	# upper = np.array([h_max, s_max, v_max])

	# lower = np.array(myColors[1][0:3])
	# upper = np.array(myColors[1][3:6])
	# mask = cv2.inRange(imgHSV, lower, upper)
	# cv2.imshow('img', mask)

	count = 0
	newPoints=[]
	for color in myColors:
		lower = np.array(color[0:3])
		upper = np.array(color[3:6])
		mask = cv2.inRange(imgHSV, lower, upper)
		x, y = getContours(mask)
		cv2.circle(imgResult, (x,y), 10, myColorsValue[count], cv2.FILLED)
		if x !=0 and y!=0:
			newPoints.append([x,y,count])
		count +=1
		# cv2.imshow(str(color[0]), mask)

	return newPoints


def getContours(img):
	contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	x, y, w, h = 0,0,0,0
	for cnt in contours:
		area = cv2.contourArea(cnt)
		if area > 500:
			# cv2.drawContours(imgResult, cnt, -1, (255,0,0), 3)
			peri = cv2.arcLength(cnt, True)
			approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
			x, y, w, h = cv2.boundingRect(approx)
	return x+w//2, y

def drawOnCanvas(myPoints, myColorsValue):
	for point in myPoints:
		cv2.circle(imgResult, (point[0],point[1]), 10, myColorsValue[point[2]], cv2.FILLED)


while cap.isOpened():
	success, img = cap.read()
	imgResult = img.copy()
	newPoints = findColor(img, myColors, myColorsValue)

	if len(newPoints)!=0:
		for newP in newPoints:
			myPoints.append(newP)
	if len(myPoints)!=0:
		drawOnCanvas(myPoints, myColorsValue)

	cv2.imshow("result", imgResult)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


cap.release()
cv2.destroyAllWindows()