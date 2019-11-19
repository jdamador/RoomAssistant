import tensorflow as tf
import numpy as np
from cv2 import cv2
from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import label_map_util
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('INFO')


def detect():
    # Number of diffent objects that the system can identify.
    NUM_CLASSES = 1
    # Load the labels of tag to put in each object indenfied.
    label_map = label_map_util.load_labelmap('tools/training/labelmap.pbtxt')
    # Convert the labels into a label map for each object class.
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile('tools/inference_graph/frozen_inference_graph.pb', 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.compat.v1.Session(graph=detection_graph)

    # Define input and output tensors (i.e. data) for the object detection classifier

    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name(
        'detection_classes:0')

    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    # Load image using OpenCV and
    image = cv2.imread('img.jpg')
    image_expanded = np.expand_dims(image, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    # Draw the results of the detection (aka 'visualize the results')
    image, count = vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.60)
    return count
    # print(count, "this is a counter")
    # try:
    #     font = cv2.cv2.FONT_HERSHEY_SIMPLEX
    #     cv2.cv2.putText(
    #         image,
    #         'People count: ' + str(count),
    #         (10, 35),
    #         font,
    #         0.8,
    #         (0, 0xFF, 0xFF),
    #         2,
    #         cv2.FONT_HERSHEY_SIMPLEX,
    #     )
    # except:
    #     pass
    # # All the results have been drawn on the image. Now display the image.
    # imS = cv2.resize(image, (960, 540))
    # cv2.imshow('Object detector', imS)

    # # Press any key to close the image
    # cv2.waitKey(0)

    # # Clean up
    # cv2.destroyAllWindows()


# * This function return a state of a room using a picture from a ip camera.
def getStatus(url):
    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()
    cv2.imwrite('img.jpg', frame)
    return detect()

if __name__ == "__main__":
  pass

#getStatus('http://compu:ICSCcomputec@172.24.15.126/mjpg/video.mjpg')