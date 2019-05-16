#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 12:02:10 2018

@author: insanesac
"""

graph = 'model/frozen_inference_graph.pb'
label = 'model/labels.pbtxt'

NUM_CLASSES = 2

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(graph, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(label)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
sess = tf.Session(graph=detection_graph)
dummy_image = np.zeros((200,200,3))

dummy_image_expanded = np.expand_dims(dummy_image, axis=0)



image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

(boxes, scores, classes, num) = sess.run(
  [detection_boxes, detection_scores, detection_classes, num_detections],
  feed_dict={image_tensor: dummy_image_expanded})


def load_image_into_numpy_array(image):
          (im_width, im_height) = image.size
          return np.array(image.getdata()).reshape(
              (im_height, im_width, 3)).astype(np.uint8)
          
class TagDetection:
    def detect_tag(self,img):
        start_time = time.time()
        print("222222222222222")
        status_m = False
        status_b = True
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        
        
        image = Image.fromarray(img)
        tn_image = image
        image_new = np.array(tn_image)
        tn_image_width, tn_image_height = image.size
        maxsize = (400, 400)
        image.thumbnail(maxsize, Image.ANTIALIAS)
        image_width, image_height = image.size
        
        image_np_expanded = np.expand_dims(img, axis=0)
        (boxes, scores, classes, num) = sess.run(
          [detection_boxes, detection_scores, detection_classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})

        boxes = np.squeeze(boxes)
        classes = np.squeeze(classes)
        scores = np.squeeze(scores)
        
        for index, score in enumerate(scores):
          if score < 0.5:
            continue

          label_name = category_index[classes[index]]['name']
          ymin, xmin, ymax, xmax = boxes[index]
          (left, right, top, bottom) = (xmin * tn_image_width, xmax * tn_image_width,
                                  ymin * tn_image_height, ymax * tn_image_height)
        
          if label_name == 'Brand_Tag':
            roi_b = image_new[int(top)-10:int(bottom)+10,int(left)-10:int(right)+10,:]
            r,c = roi_b.shape[0:2]
            if r == 0 or c == 0:
                  roi_b = image_new[int(top):int(bottom),int(left):int(right),:]
            status_b = True
#          
          elif label_name == 'Myntra_Tag': 
              roi_m = image_new[int(top)-10:int(bottom)+10,int(left)-10:int(right)+10,:]
              r,c = roi_m.shape[0:2]
              if r == 0 or c == 0:
                  roi_m = image_new[int(top):int(bottom),int(left):int(right),:]
              status_m = True

        end_time = time.time() - start_time
        print("tagTime taken:", end_time)
#        bar_status = 'none'

        roi_myntra = barcode_cor_myntra(roi_m)
        roi_brand = barcode_cor_brand(roi_b)
        cv2.imwrite("static/roi/roi_m_cropped.jpg",roi_myntra)
        cv2.imwrite("static/roi/roi_b_cropped.jpg",roi_brand) 
#        cv2.imwrite("static/roi/roi_m_cropped.jpg",roi_brand)
        start_time = time.time()
        roi_cropped,myntra_text = MyntraOcr().extract_text(roi_myntra)
        end_time = time.time() - start_time
        print("myntra Time taken:", end_time)
        start_time1 = time.time()
        brand_text = BrandOcr.text_extract(roi_brand)
        end_time1 = time.time() - start_time1
        print("brand Time taken:", end_time1)
        barcode = BarcodeReader(None,roi_cropped)
        if barcode.exists:
            bar_status = "barcode"
            print("bar status code",bar_status)
            return barcode,bar_status,myntra_text,brand_text
        elif  type(myntra_text) == dict:
            barcode = myntra_text["barcode"]
            bar_status = "text"
            return barcode,bar_status,myntra_text,brand_text
#
#path = r'/home/pramod/workspace/outward-qc/calib/col4.jpg'
#img = cv2.imread(path)
#TagDetection().detect_tag(img)

