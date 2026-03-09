"use client";

interface GaltungTriangleProps {
  direct: boolean;
  structural: boolean;
  cultural: boolean;
  size?: number;
}

export function GaltungTriangle({
  direct,
  structural,
  cultural,
  size = 160,
}: GaltungTriangleProps) {
  const h = size * 0.87;
  const cx = size / 2;
  const pad = 12;

  const topX = cx;
  const topY = pad;
  const bottomLeftX = pad;
  const bottomLeftY = h - pad;
  const bottomRightX = size - pad;
  const bottomRightY = h - pad;

  const activeColor = "#dc2626";
  const inactiveColor = "#333";
  const activeGlow = "drop-shadow(0 0 6px rgba(220, 38, 38, 0.6))";

  return (
    <svg
      width={size}
      height={h + 20}
      viewBox={`0 0 ${size} ${h + 20}`}
      className="galtung-triangle"
    >
      <line
        x1={topX}
        y1={topY}
        x2={bottomLeftX}
        y2={bottomLeftY}
        stroke={direct || cultural ? activeColor : inactiveColor}
        strokeWidth={2}
        opacity={0.4}
      />
      <line
        x1={topX}
        y1={topY}
        x2={bottomRightX}
        y2={bottomRightY}
        stroke={direct || structural ? activeColor : inactiveColor}
        strokeWidth={2}
        opacity={0.4}
      />
      <line
        x1={bottomLeftX}
        y1={bottomLeftY}
        x2={bottomRightX}
        y2={bottomRightY}
        stroke={cultural || structural ? activeColor : inactiveColor}
        strokeWidth={2}
        opacity={0.4}
      />

      {/* Direct - top vertex */}
      <circle
        cx={topX}
        cy={topY}
        r={8}
        fill={direct ? activeColor : inactiveColor}
        style={{ filter: direct ? activeGlow : "none" }}
      />
      <text
        x={topX}
        y={topY - 14}
        textAnchor="middle"
        fill={direct ? "#fca5a5" : "#666"}
        className="font-mono"
        fontSize="10"
      >
        DIRECT
      </text>

      {/* Cultural - bottom left */}
      <circle
        cx={bottomLeftX}
        cy={bottomLeftY}
        r={8}
        fill={cultural ? activeColor : inactiveColor}
        style={{ filter: cultural ? activeGlow : "none" }}
      />
      <text
        x={bottomLeftX}
        y={bottomLeftY + 18}
        textAnchor="middle"
        fill={cultural ? "#fde68a" : "#666"}
        className="font-mono"
        fontSize="10"
      >
        CULTURAL
      </text>

      {/* Structural - bottom right */}
      <circle
        cx={bottomRightX}
        cy={bottomRightY}
        r={8}
        fill={structural ? activeColor : inactiveColor}
        style={{ filter: structural ? activeGlow : "none" }}
      />
      <text
        x={bottomRightX}
        y={bottomRightY + 18}
        textAnchor="middle"
        fill={structural ? "#fed7aa" : "#666"}
        className="font-mono"
        fontSize="10"
      >
        STRUCTURAL
      </text>
    </svg>
  );
}
