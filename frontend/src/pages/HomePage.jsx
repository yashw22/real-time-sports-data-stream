import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchLiveMatches } from "../api";
import CategoryCard from "../components/CategoryCard";

const HomePage = () => {
  const [categories, setCategories] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    const loadCategories = async () => {
      const data = await fetchLiveMatches();
      const categoryCount = data.reduce((acc, obj) => {
        const { topic } = obj;
        acc[topic] = (acc[topic] || 0) + 1;
        return acc;
      }, {});
      setCategories(categoryCount);
    };

    loadCategories();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-6 flex justify-center">
        Live Sports
      </h1>
      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {Object.entries(categories).map(([topic, count]) => (
          <CategoryCard
            key={topic}
            topic={topic}
            count={count}
            onClick={() => navigate(`/sport/${topic}`)}
          />
        ))}
      </div>
    </div>
  );
};

export default HomePage;
