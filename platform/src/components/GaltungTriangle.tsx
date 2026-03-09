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

  const activeColor = "#b91c1c";
  const inactiveColor = "#d6d3d1";

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
        strokeWidth={1.5}
        opacity={0.5}
      />
      <line
        x1={topX}
        y1={topY}
        x2={bottomRightX}
        y2={bottomRightY}
        stroke={direct || structural ? activeColor : inactiveColor}
        strokeWidth={1.5}
        opacity={0.5}
      />
      <line
        x1={bottomLeftX}
        y1={bottomLeftY}
        x2={bottomRightX}
        y2={bottomRightY}
        stroke={cultural || structural ? activeColor : inactiveColor}
        strokeWidth={1.5}
        opacity={0.5}
      />

      <circle
        cx={topX}
        cy={topY}
        r={7}
        fill={direct ? activeColor : inactiveColor}
      />
      <text
        x={topX}
        y={topY - 12}
        textAnchor="middle"
        fill={direct ? "#b91c1c" : "#a8a29e"}
        className="font-mono"
        fontSize="9"
      >
        DIRECT
      </text>

      <circle
        cx={bottomLeftX}
        cy={bottomLeftY}
        r={7}
        fill={cultural ? activeColor : inactiveColor}
      />
      <text
        x={bottomLeftX}
        y={bottomLeftY + 16}
        textAnchor="middle"
        fill={cultural ? "#b91c1c" : "#a8a29e"}
        className="font-mono"
        fontSize="9"
      >
        CULTURAL
      </text>

      <circle
        cx={bottomRightX}
        cy={bottomRightY}
        r={7}
        fill={structural ? activeColor : inactiveColor}
      />
      <text
        x={bottomRightX}
        y={bottomRightY + 16}
        textAnchor="middle"
        fill={structural ? "#b91c1c" : "#a8a29e"}
        className="font-mono"
        fontSize="9"
      >
        STRUCTURAL
      </text>
    </svg>
  );
}
