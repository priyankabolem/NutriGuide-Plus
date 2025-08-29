"""
Advanced Color Histogram Analysis for Food Recognition
Uses RGB, HSV, and CIELab color spaces for accurate food identification
"""
import base64
import io
import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Optional
import cv2
from scipy.spatial.distance import euclidean, cosine
from collections import defaultdict
import colorsys

class ColorHistogramAnalyzer:
    def __init__(self):
        # Pre-computed color signatures for common foods
        self.food_color_signatures = {
            "pizza": {
                "dominant_hues": [(0, 10), (40, 60)],  # Red and yellow hues
                "saturation_range": (0.3, 0.8),
                "brightness_range": (0.3, 0.7),
                "lab_clusters": [
                    {"L": 50, "a": 20, "b": 20},  # Tomato red
                    {"L": 70, "a": 5, "b": 40},   # Cheese yellow
                    {"L": 40, "a": 10, "b": 15}   # Crust brown
                ]
            },
            "salad": {
                "dominant_hues": [(80, 140)],  # Green hues
                "saturation_range": (0.3, 0.8),
                "brightness_range": (0.3, 0.6),
                "lab_clusters": [
                    {"L": 50, "a": -30, "b": 30},  # Leafy green
                    {"L": 60, "a": -20, "b": 40},  # Light green
                    {"L": 40, "a": -25, "b": 25}   # Dark green
                ]
            },
            "burger": {
                "dominant_hues": [(20, 40)],  # Brown hues
                "saturation_range": (0.2, 0.6),
                "brightness_range": (0.2, 0.5),
                "lab_clusters": [
                    {"L": 40, "a": 15, "b": 20},   # Meat brown
                    {"L": 60, "a": 5, "b": 30},    # Bun brown
                    {"L": 70, "a": 0, "b": 40}     # Light bun
                ]
            },
            "sushi": {
                "dominant_hues": [(0, 20), (160, 200)],  # Red (fish) and blue-green (nori)
                "saturation_range": (0.2, 0.7),
                "brightness_range": (0.4, 0.8),
                "lab_clusters": [
                    {"L": 80, "a": 0, "b": 0},     # White rice
                    {"L": 50, "a": 30, "b": 10},   # Salmon
                    {"L": 30, "a": -5, "b": -10}   # Nori (seaweed)
                ]
            },
            "rice": {
                "dominant_hues": [(40, 60)],  # Light yellow/beige
                "saturation_range": (0.0, 0.2),
                "brightness_range": (0.7, 0.95),
                "lab_clusters": [
                    {"L": 85, "a": 0, "b": 10},    # White rice
                    {"L": 75, "a": 5, "b": 15},    # Fried rice
                    {"L": 80, "a": 2, "b": 12}     # Steamed rice
                ]
            },
            "curry": {
                "dominant_hues": [(20, 40)],  # Orange/yellow hues
                "saturation_range": (0.5, 0.9),
                "brightness_range": (0.4, 0.7),
                "lab_clusters": [
                    {"L": 60, "a": 20, "b": 50},   # Curry yellow
                    {"L": 50, "a": 30, "b": 40},   # Curry orange
                    {"L": 45, "a": 25, "b": 35}    # Dark curry
                ]
            },
            "steak": {
                "dominant_hues": [(0, 20), (340, 360)],  # Red-brown hues
                "saturation_range": (0.3, 0.7),
                "brightness_range": (0.2, 0.5),
                "lab_clusters": [
                    {"L": 35, "a": 20, "b": 15},   # Rare red
                    {"L": 40, "a": 15, "b": 20},   # Medium brown
                    {"L": 30, "a": 10, "b": 10}    # Well-done dark
                ]
            },
            "pasta": {
                "dominant_hues": [(40, 60)],  # Yellow/beige for plain pasta
                "saturation_range": (0.2, 0.6),
                "brightness_range": (0.5, 0.8),
                "lab_clusters": [
                    {"L": 70, "a": 5, "b": 40},    # Plain pasta
                    {"L": 55, "a": 25, "b": 25},   # Tomato sauce
                    {"L": 80, "a": 0, "b": 20}     # Cream sauce
                ]
            },
            "fruit": {
                "dominant_hues": [(0, 60), (280, 340)],  # Red, orange, yellow, purple
                "saturation_range": (0.5, 0.9),
                "brightness_range": (0.4, 0.8),
                "lab_clusters": [
                    {"L": 60, "a": 40, "b": 20},   # Red fruits
                    {"L": 70, "a": 10, "b": 60},   # Yellow fruits
                    {"L": 65, "a": 30, "b": 50}    # Orange fruits
                ]
            },
            "eggs": {
                "dominant_hues": [(40, 60)],  # Yellow yolk
                "saturation_range": (0.4, 0.8),
                "brightness_range": (0.7, 0.95),
                "lab_clusters": [
                    {"L": 85, "a": 0, "b": 50},    # Yolk yellow
                    {"L": 90, "a": 0, "b": 5},     # White
                    {"atter": 75, "a": 5, "b": 30}   # Cooked egg
                ]
            }
        }
        
        # Color space bins for histogram computation
        self.hsv_bins = {
            'h': 36,  # 36 bins for hue (0-360 degrees)
            's': 8,   # 8 bins for saturation
            'v': 8    # 8 bins for value (brightness)
        }
        
        self.lab_bins = {
            'l': 10,  # 10 bins for lightness
            'a': 20,  # 20 bins for green-red
            'b': 20   # 20 bins for blue-yellow
        }
    
    def analyze_food_image(self, image_b64: str) -> Tuple[str, float, Dict]:
        """Analyze food image using advanced color histogram techniques"""
        try:
            # Decode image
            img = self._decode_image(image_b64)
            
            # Convert to different color spaces
            img_rgb = np.array(img)
            img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
            img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
            
            # Compute histograms
            hist_rgb = self._compute_rgb_histogram(img_rgb)
            hist_hsv = self._compute_hsv_histogram(img_hsv)
            hist_lab = self._compute_lab_histogram(img_lab)
            
            # Extract color features
            features = {
                'rgb_histogram': hist_rgb,
                'hsv_histogram': hist_hsv,
                'lab_histogram': hist_lab,
                'dominant_colors': self._extract_dominant_colors(img_rgb),
                'color_moments': self._compute_color_moments(img_rgb),
                'hsv_features': self._extract_hsv_features(img_hsv),
                'lab_features': self._extract_lab_features(img_lab)
            }
            
            # Match against food signatures
            best_match, confidence = self._match_food_signatures(features)
            
            # If confidence is low, try clustering approach
            if confidence < 0.7:
                cluster_match, cluster_confidence = self._cluster_based_matching(img_rgb, features)
                if cluster_confidence > confidence:
                    best_match = cluster_match
                    confidence = cluster_confidence
            
            return (best_match, confidence, features)
            
        except Exception as e:
            print(f"Color histogram analysis error: {e}")
            return ("unidentified food", 0.5, {})
    
    def _decode_image(self, image_b64: str) -> Image.Image:
        """Decode base64 image"""
        img_bytes = base64.b64decode(image_b64)
        return Image.open(io.BytesIO(img_bytes)).convert('RGB')
    
    def _compute_rgb_histogram(self, img_rgb: np.ndarray) -> Dict:
        """Compute normalized RGB histogram"""
        hist_r = cv2.calcHist([img_rgb], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([img_rgb], [1], None, [256], [0, 256])
        hist_b = cv2.calcHist([img_rgb], [2], None, [256], [0, 256])
        
        # Normalize
        hist_r = hist_r.flatten() / hist_r.sum()
        hist_g = hist_g.flatten() / hist_g.sum()
        hist_b = hist_b.flatten() / hist_b.sum()
        
        return {
            'r': hist_r,
            'g': hist_g,
            'b': hist_b,
            'combined': np.concatenate([hist_r, hist_g, hist_b])
        }
    
    def _compute_hsv_histogram(self, img_hsv: np.ndarray) -> Dict:
        """Compute HSV histogram with proper binning"""
        # Compute 3D histogram
        hist_3d = cv2.calcHist(
            [img_hsv], [0, 1, 2], None,
            [self.hsv_bins['h'], self.hsv_bins['s'], self.hsv_bins['v']],
            [0, 180, 0, 256, 0, 256]
        )
        
        # Normalize
        hist_3d = hist_3d.flatten() / hist_3d.sum()
        
        # Also compute individual channel histograms
        hist_h = cv2.calcHist([img_hsv], [0], None, [180], [0, 180])
        hist_s = cv2.calcHist([img_hsv], [1], None, [256], [0, 256])
        hist_v = cv2.calcHist([img_hsv], [2], None, [256], [0, 256])
        
        return {
            'h': hist_h.flatten() / hist_h.sum(),
            's': hist_s.flatten() / hist_s.sum(),
            'v': hist_v.flatten() / hist_v.sum(),
            '3d': hist_3d
        }
    
    def _compute_lab_histogram(self, img_lab: np.ndarray) -> Dict:
        """Compute CIELab histogram"""
        # Compute 3D histogram
        hist_3d = cv2.calcHist(
            [img_lab], [0, 1, 2], None,
            [self.lab_bins['l'], self.lab_bins['a'], self.lab_bins['b']],
            [0, 256, 0, 256, 0, 256]
        )
        
        # Normalize
        hist_3d = hist_3d.flatten() / hist_3d.sum()
        
        return {
            '3d': hist_3d,
            'l_mean': np.mean(img_lab[:, :, 0]),
            'a_mean': np.mean(img_lab[:, :, 1]),
            'b_mean': np.mean(img_lab[:, :, 2])
        }
    
    def _extract_dominant_colors(self, img_rgb: np.ndarray, k=5) -> List[Dict]:
        """Extract dominant colors using k-means clustering"""
        # Reshape image to list of pixels
        pixels = img_rgb.reshape(-1, 3)
        
        # Sample pixels for efficiency
        if len(pixels) > 10000:
            indices = np.random.choice(len(pixels), 10000, replace=False)
            pixels = pixels[indices]
        
        # K-means clustering
        try:
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(pixels)
        except ImportError:
            # Fallback to simple dominant color extraction without sklearn
            # Calculate average colors in different regions
            colors = []
            labels = []
            
            # Simple color quantization
            for i in range(k):
                start_idx = i * len(pixels) // k
                end_idx = (i + 1) * len(pixels) // k
                cluster_pixels = pixels[start_idx:end_idx]
                if len(cluster_pixels) > 0:
                    avg_color = np.mean(cluster_pixels, axis=0)
                    colors.append(avg_color)
                    labels.extend([i] * len(cluster_pixels))
            
            colors = np.array(colors)
            labels = np.array(labels[:len(pixels)])
            
            class SimpleKMeans:
                def __init__(self):
                    self.cluster_centers_ = colors
                    self.labels_ = labels
            
            kmeans = SimpleKMeans()
        
        # Get cluster centers and sizes
        colors = kmeans.cluster_centers_
        labels = kmeans.labels_
        
        # Calculate percentage of each cluster
        dominant_colors = []
        for i in range(k):
            count = np.sum(labels == i)
            percentage = count / len(labels)
            
            color_rgb = colors[i].astype(int)
            color_hsv = colorsys.rgb_to_hsv(
                color_rgb[0]/255, color_rgb[1]/255, color_rgb[2]/255
            )
            
            dominant_colors.append({
                'rgb': color_rgb.tolist(),
                'hsv': [color_hsv[0]*360, color_hsv[1], color_hsv[2]],
                'percentage': percentage
            })
        
        # Sort by percentage
        dominant_colors.sort(key=lambda x: x['percentage'], reverse=True)
        
        return dominant_colors
    
    def _compute_color_moments(self, img_rgb: np.ndarray) -> Dict:
        """Compute color moments (mean, std, skewness) for each channel"""
        from scipy import stats
        
        moments = {}
        for i, channel in enumerate(['r', 'g', 'b']):
            pixels = img_rgb[:, :, i].flatten()
            moments[channel] = {
                'mean': np.mean(pixels),
                'std': np.std(pixels),
                'skewness': stats.skew(pixels)
            }
        
        return moments
    
    def _extract_hsv_features(self, img_hsv: np.ndarray) -> Dict:
        """Extract HSV-specific features"""
        h_channel = img_hsv[:, :, 0]
        s_channel = img_hsv[:, :, 1]
        v_channel = img_hsv[:, :, 2]
        
        # Convert hue to degrees
        h_degrees = h_channel * 2  # OpenCV uses 0-180 for hue
        
        # Find dominant hue ranges
        hue_histogram = np.histogram(h_degrees, bins=36, range=(0, 360))[0]
        dominant_hues = np.argsort(hue_histogram)[-3:]  # Top 3 hue bins
        
        features = {
            'dominant_hues': dominant_hues.tolist(),
            'avg_saturation': np.mean(s_channel) / 255,
            'avg_brightness': np.mean(v_channel) / 255,
            'saturation_std': np.std(s_channel) / 255,
            'brightness_std': np.std(v_channel) / 255
        }
        
        return features
    
    def _extract_lab_features(self, img_lab: np.ndarray) -> Dict:
        """Extract Lab color space features"""
        l_channel = img_lab[:, :, 0]
        a_channel = img_lab[:, :, 1]
        b_channel = img_lab[:, :, 2]
        
        features = {
            'l_range': (np.min(l_channel), np.max(l_channel)),
            'a_range': (np.min(a_channel), np.max(a_channel)),
            'b_range': (np.min(b_channel), np.max(b_channel)),
            'color_variance': np.var(img_lab.reshape(-1, 3), axis=0).tolist()
        }
        
        return features
    
    def _match_food_signatures(self, features: Dict) -> Tuple[str, float]:
        """Match extracted features against known food signatures"""
        best_match = None
        best_score = 0
        
        hsv_features = features.get('hsv_features', {})
        lab_features = features.get('lab_features', {})
        dominant_colors = features.get('dominant_colors', [])
        
        for food_name, signature in self.food_color_signatures.items():
            score = 0
            matches = 0
            
            # Check HSV features
            if hsv_features:
                # Check dominant hues
                detected_hues = hsv_features.get('dominant_hues', [])
                for hue_range in signature['dominant_hues']:
                    for detected_hue in detected_hues:
                        hue_degree = detected_hue * 10  # Convert bin to degree
                        if hue_range[0] <= hue_degree <= hue_range[1]:
                            score += 0.3
                            matches += 1
                            break
                
                # Check saturation
                avg_sat = hsv_features.get('avg_saturation', 0)
                if signature['saturation_range'][0] <= avg_sat <= signature['saturation_range'][1]:
                    score += 0.2
                    matches += 1
                
                # Check brightness
                avg_bright = hsv_features.get('avg_brightness', 0)
                if signature['brightness_range'][0] <= avg_bright <= signature['brightness_range'][1]:
                    score += 0.2
                    matches += 1
            
            # Check Lab clusters
            if lab_features and dominant_colors:
                lab_mean_a = lab_features.get('a_range', [0, 0])
                lab_mean_b = lab_features.get('b_range', [0, 0])
                
                for lab_cluster in signature.get('lab_clusters', []):
                    # Check if detected colors are close to expected clusters
                    for dom_color in dominant_colors[:3]:  # Check top 3 dominant colors
                        # Simple proximity check
                        if (abs(lab_mean_a[0] - lab_cluster['a']) < 30 and 
                            abs(lab_mean_b[0] - lab_cluster['b']) < 30):
                            score += 0.1
                            matches += 1
                            break
            
            # Normalize score
            if matches > 0:
                normalized_score = score / max(1, len(signature.get('dominant_hues', [1])) + 2)
                if normalized_score > best_score:
                    best_score = normalized_score
                    best_match = food_name
        
        # Convert score to confidence
        confidence = min(0.95, 0.5 + best_score)
        
        if not best_match:
            # Fallback based on dominant colors
            if dominant_colors:
                dom_hsv = dominant_colors[0]['hsv']
                hue = dom_hsv[0]
                
                if 80 <= hue <= 140:  # Green
                    best_match = "salad"
                elif (0 <= hue <= 20) or (340 <= hue <= 360):  # Red
                    best_match = "tomato dish"
                elif 40 <= hue <= 60:  # Yellow
                    best_match = "pasta"
                else:
                    best_match = "mixed dish"
                
                confidence = 0.65
        
        return (best_match or "unidentified food", confidence)
    
    def _cluster_based_matching(self, img_rgb: np.ndarray, features: Dict) -> Tuple[str, float]:
        """Alternative matching using color clustering patterns"""
        dominant_colors = features.get('dominant_colors', [])
        
        if not dominant_colors:
            return ("mixed dish", 0.5)
        
        # Analyze color patterns
        top_color = dominant_colors[0]
        top_hsv = top_color['hsv']
        hue = top_hsv[0]
        saturation = top_hsv[1]
        brightness = top_hsv[2]
        
        # Pattern-based recognition
        if len(dominant_colors) >= 3:
            # Multi-colored foods
            color_diversity = len(set(c['hsv'][0] // 30 for c in dominant_colors[:3]))
            
            if color_diversity >= 3:
                # High color diversity suggests complex dishes
                if any(80 <= c['hsv'][0] <= 140 for c in dominant_colors[:3]):  # Has green
                    return ("salad", 0.75)
                elif any((0 <= c['hsv'][0] <= 20) or (340 <= c['hsv'][0] <= 360) 
                        for c in dominant_colors[:3]):  # Has red
                    return ("pizza", 0.70)
                else:
                    return ("mixed plate", 0.65)
            elif color_diversity == 2:
                # Two main colors
                if saturation > 0.5 and brightness > 0.5:
                    return ("curry", 0.70)
                else:
                    return ("rice dish", 0.68)
        
        # Single dominant color patterns
        if saturation < 0.2 and brightness > 0.7:
            return ("rice", 0.75)
        elif 20 <= hue <= 40 and saturation > 0.4:
            return ("curry", 0.72)
        elif 80 <= hue <= 140 and saturation > 0.3:
            return ("vegetables", 0.70)
        elif hue < 20 or hue > 340:
            if brightness < 0.4:
                return ("steak", 0.68)
            else:
                return ("tomato dish", 0.66)
        else:
            return ("cooked dish", 0.60)

# Global instance
color_analyzer = ColorHistogramAnalyzer()

def analyze_food_with_color_histograms(image_b64: str) -> Tuple[str, float, Dict]:
    """Public API for color histogram analysis"""
    return color_analyzer.analyze_food_image(image_b64)