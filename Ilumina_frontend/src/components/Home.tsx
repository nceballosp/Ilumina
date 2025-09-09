import React from 'react';

interface HomeProps {
  title: string;
}

export const Home: React.FC<HomeProps> = ({ title }) => {
  return (
    <div className="flex justify-center bg-iluminab max-w-full min-h-screen">
      {title}
      <h1 className="font-bold text-2xl text-white pt-8 pb-8">
        Bienvenido a Ilumina Beta 0.0.0
      </h1>
    </div>
  );
};
