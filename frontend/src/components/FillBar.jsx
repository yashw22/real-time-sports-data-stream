/* eslint-disable react/prop-types */
const FillBar = ({ duration }) => {
  const animationStyle = {
    animation: `fillBar ${duration}s linear`,
  };

  return (
    <div className="w-full bg-gray-200 h-1 rounded-full overflow-hidden">
      <div className="bar bg-green-500 h-full" style={animationStyle}></div>
    </div>
  );
};

export default FillBar;
