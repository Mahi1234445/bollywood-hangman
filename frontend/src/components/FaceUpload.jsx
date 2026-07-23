import { useRef, useState, useCallback } from "react";

const DISPLAY_SIZE = 260; // px, the cropping preview box
const OUTPUT_SIZE = 240; // px, the exported circular face image

export default function FaceUpload({ onFaceReady, onSkip }) {
  const [imgSrc, setImgSrc] = useState(null);
  const [natural, setNatural] = useState({ w: 0, h: 0 });
  const [circle, setCircle] = useState({ cx: DISPLAY_SIZE / 2, cy: DISPLAY_SIZE / 2, r: 70 });
  const dragging = useRef(false);
  const imgRef = useRef(null);
  const containerRef = useRef(null);

  const onFile = useCallback((e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setImgSrc(reader.result);
    reader.readAsDataURL(file);
  }, []);

  const onImgLoad = useCallback((e) => {
    setNatural({ w: e.target.naturalWidth, h: e.target.naturalHeight });
  }, []);

  const clampCenter = (cx, cy, r) => ({
    cx: Math.min(Math.max(cx, r), DISPLAY_SIZE - r),
    cy: Math.min(Math.max(cy, r), DISPLAY_SIZE - r),
    r,
  });

  const startDrag = () => (dragging.current = true);
  const stopDrag = () => (dragging.current = false);

  const onMove = useCallback((e) => {
    if (!dragging.current || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const x = clientX - rect.left;
    const y = clientY - rect.top;
    setCircle((c) => clampCenter(x, y, c.r));
  }, []);

  const onZoom = useCallback((e) => {
    const r = Number(e.target.value);
    setCircle((c) => clampCenter(c.cx, c.cy, r));
  }, []);

  const confirmCrop = useCallback(() => {
    if (!imgRef.current || natural.w === 0) return;
    const scale = natural.w / DISPLAY_SIZE;
    const sx = (circle.cx - circle.r) * scale;
    const sy = (circle.cy - circle.r) * scale;
    const sSize = circle.r * 2 * scale;

    const canvas = document.createElement("canvas");
    canvas.width = OUTPUT_SIZE;
    canvas.height = OUTPUT_SIZE;
    const ctx = canvas.getContext("2d");
    ctx.save();
    ctx.beginPath();
    ctx.arc(OUTPUT_SIZE / 2, OUTPUT_SIZE / 2, OUTPUT_SIZE / 2, 0, Math.PI * 2);
    ctx.closePath();
    ctx.clip();
    ctx.drawImage(imgRef.current, sx, sy, sSize, sSize, 0, 0, OUTPUT_SIZE, OUTPUT_SIZE);
    ctx.restore();

    onFaceReady(canvas.toDataURL("image/png"));
  }, [circle, natural, onFaceReady]);

  return (
    <div className="face-upload">
      {!imgSrc && (
        <>
          <p className="face-upload-copy">
            Upload a photo and your face goes up on the gallows instead of a
            plain stick figure head.
          </p>
          <label className="file-btn">
            Choose photo
            <input type="file" accept="image/*" onChange={onFile} hidden />
          </label>
          <button className="skip-link" onClick={onSkip}>
            Skip — use a default head
          </button>
        </>
      )}

      {imgSrc && (
        <>
          <div
            className="crop-container"
            ref={containerRef}
            style={{ width: DISPLAY_SIZE, height: DISPLAY_SIZE }}
            onMouseMove={onMove}
            onMouseUp={stopDrag}
            onMouseLeave={stopDrag}
            onTouchMove={onMove}
            onTouchEnd={stopDrag}
          >
            <img
              ref={imgRef}
              src={imgSrc}
              onLoad={onImgLoad}
              alt="Uploaded, position the circle over your face"
              className="crop-img"
              style={{ width: DISPLAY_SIZE }}
            />
            <div
              className="crop-circle"
              style={{
                left: circle.cx - circle.r,
                top: circle.cy - circle.r,
                width: circle.r * 2,
                height: circle.r * 2,
              }}
              onMouseDown={startDrag}
              onTouchStart={startDrag}
            />
          </div>
          <input
            type="range"
            min="30"
            max="130"
            value={circle.r}
            onChange={onZoom}
            className="zoom-slider"
          />
          <div className="crop-actions">
            <button className="play-btn" onClick={confirmCrop}>Use this face</button>
            <button className="skip-link" onClick={() => setImgSrc(null)}>Choose a different photo</button>
          </div>
        </>
      )}
    </div>
  );
}
