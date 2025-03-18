export function Card({ className, children }) {
    return (
      <div className={`bg-white shadow-md rounded-lg p-4 ${className}`}>
        {children}
      </div>
    );
  }
  
  export function CardContent({ className, children }) {
    return <div className={`p-2 ${className}`}>{children}</div>;
  }
  