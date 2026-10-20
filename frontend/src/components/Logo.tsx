
import Link from "next/link";

export default function Logo({
  compact = false,
}: {
  compact?: boolean;
}) {
  return (
    <Link
      href="/"
      className="flex items-center"
      aria-label="QuantumInsight home"
    >
      <img
        src="/logo.svg"
        alt="QuantumInsight"
        width={compact ? 48 : 180}
        height={compact ? 48 : 48}
        className="block h-auto object-contain"
        style={{
          width: compact ? "48px" : "180px",
          maxWidth: "100%",
        }}
      />
    </Link>
  );
}
