/* eslint-disable react/prop-types */

import { firstCharCap } from "../utils/stringUtils";

const CategoryCard = ({ topic, count, onClick }) => (
  <div
    className="bg-blue-500 text-white p-6 rounded-lg shadow-md cursor-pointer"
    onClick={onClick}
  >
    <h2 className="text-xl font-bold">{firstCharCap(topic)}</h2>
    <p>
      {count} live match{count > 1 && "es"}
    </p>
  </div>
);

export default CategoryCard;
